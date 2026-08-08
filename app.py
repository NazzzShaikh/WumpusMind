from flask import Flask, render_template, request, jsonify, session
import uuid
import os
import random

from environment import WumpusEnvironment
from agent_hybrid import HybridAgent
from agent_baselines import RandomAgent, BFSAgent, AStarAgent
from config import DIFFICULTY_PRESETS, SCORE_MOVE, SCORE_DEATH, SCORE_GOLD

app = Flask(__name__)
app.secret_key = os.urandom(24)

# In-memory store for game sessions (sufficient for single-worker or small demo deployments)
# Key: session_id, Value: {"env": WumpusEnvironment, "agent": AgentObject, "score": int, "algorithm": str}
GAMES = {}

def get_or_create_game():
    if "id" not in session or session["id"] not in GAMES:
        session["id"] = str(uuid.uuid4())
        # Default fallback game
        env = WumpusEnvironment(size=4, difficulty="Easy")
        agent = HybridAgent(4, pit_prob=0.1, wumpus_count=1)
        GAMES[session["id"]] = {"env": env, "agent": agent, "score": 0, "algorithm": "Hybrid"}
    return GAMES[session["id"]]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play')
def play():
    if "id" not in session or session["id"] not in GAMES:
        return app.redirect('/')
    return render_template('play.html')

@app.route('/learn')
def learn():
    return render_template('learn.html')

@app.route('/api/setup', methods=['POST'])
def setup():
    data = request.json
    size = data.get('size', 4)
    difficulty = data.get('difficulty', 'Easy')
    algorithm = data.get('algorithm', 'Hybrid')
    play_mode = data.get('play_mode', 'autoplay')
    
    if play_mode == 'manual':
        algorithm = 'Hybrid' # Force AI reasoning logic for Manual Play advice
    
    session["id"] = str(uuid.uuid4())
    
    env = WumpusEnvironment(size=size, difficulty=difficulty)
    cfg = DIFFICULTY_PRESETS.get(difficulty, DIFFICULTY_PRESETS["Easy"])
    
    if algorithm == "AStar":
        agent = AStarAgent(size)
    else:
        agent = HybridAgent(size, pit_prob=cfg["pit_prob"], wumpus_count=cfg["wumpus_count"])
        
    GAMES[session["id"]] = {"env": env, "agent": agent, "score": 0, "algorithm": algorithm, "play_mode": play_mode}
    
    # Process initial percepts so the reasoning log isn't empty on load
    initial_percepts = env.get_percepts((0,0))
    if hasattr(agent, "kb"):
        initial_reasoning = agent.kb.add_percepts((0,0), initial_percepts)
        GAMES[session["id"]]["initial_log"] = {
            "action": "START",
            "target": [0,0],
            "reason": "Initialization",
            "explanation": " | ".join(initial_reasoning) if initial_reasoning else "Spawned at (0,0). No hazards detected.",
            "confidence": 1.0
        }
    
    return jsonify({"status": "success", "message": "Game initialized"})

@app.route('/api/state', methods=['GET'])
def get_state():
    game = get_or_create_game()
    env = game["env"]
    agent = game["agent"]
    
    state = env.get_state_dict()
    state["score"] = game["score"]
    state["current_percepts"] = env.get_percepts(env.agent_pos)
    
    # We also send some agent specific info for UI
    agent_info = {}
    if hasattr(agent, "kb"):
        agent_info["visited"] = list(agent.kb.visited)
        agent_info["safe"] = list(agent.kb.safe)
        
    if hasattr(agent, "prob"):
        risks_dict = agent.prob.calculate_risks()
        agent_info["risks"] = [{"x": p[0], "y": p[1], "risk": r} for p, r in risks_dict.items()]
        
    initial_log = game.get("initial_log")
    if initial_log:
        agent_info["initial_log"] = initial_log
        del game["initial_log"] # Only show once on load
        
    agent_info["play_mode"] = game.get("play_mode", "autoplay")
        
    return jsonify({"env": state, "agent": agent_info})

@app.route('/api/step', methods=['POST'])
def step():
    game = get_or_create_game()
    env = game["env"]
    agent = game["agent"]
    
    data = request.get_json(silent=True) or {}
    manual_direction = data.get('manual_direction')
    
    if not env.agent_alive or env.agent_escaped:
        return jsonify({"status": "game_over"})
        
    percepts = env.get_percepts(env.agent_pos)
    
    if manual_direction:
        # 0: Right, 1: Up, 2: Left, 3: Down
        dir_map = {"RIGHT": 0, "UP": 1, "LEFT": 2, "DOWN": 3}
        target_dir = dir_map.get(manual_direction.upper(), env.agent_dir)
        
        dx, dy = 0, 0
        if target_dir == 0: dx = 1
        elif target_dir == 1: dy = 1
        elif target_dir == 2: dx = -1
        elif target_dir == 3: dy = -1
        
        env.agent_dir = target_dir
        if hasattr(agent, 'dir'):
            agent.dir = target_dir
            
        action = "FORWARD"
        
        # We still want to see what AI would have done
        decision = agent.get_action(percepts)
        
        decision["is_manual"] = True
        decision["manual_direction"] = manual_direction
        decision["ai_action"] = decision["action"]
        decision["ai_explanation"] = decision["explanation"]
        decision["result_text"] = "Safe move."
        
        if hasattr(agent, 'pos'):
            agent.pos = (env.agent_pos[0] + dx, env.agent_pos[1] + dy)
    else:
        # Agent decides action
        decision = agent.get_action(percepts)
        action = decision["action"]
        
        env.agent_dir = agent.dir
        env.agent_pos = agent.pos
        agent.update_agent_state(action)
    
    game["score"] += SCORE_MOVE
    
    # Process consequences of movement
    new_pos = agent.pos if hasattr(agent, 'pos') else env.agent_pos
    if not env.is_valid_pos(new_pos):
        # Revert movement (hit a wall)
        if hasattr(agent, 'pos'):
            agent.pos = env.agent_pos
        if hasattr(agent, 'action_queue'):
            agent.action_queue = [] # clear queue on failure
        if decision.get("is_manual"):
            decision["result_text"] = "Hit a wall! Move reverted."
    else:
        env.agent_pos = new_pos
        if hasattr(agent, 'kb'):
            agent.kb.visited.add(new_pos)
            
        # Check hazards
        if env.grid[new_pos]["pit"] or env.grid[new_pos]["wumpus"]:
            env.agent_alive = False
            game["score"] += SCORE_DEATH
            decision["reason"] += " (DEATH)"
            decision["explanation"] += " Walked into a hazard and died!"
            if decision.get("is_manual"):
                decision["result_text"] = "Hazard! You walked into a pit or Wumpus. Game over."
        else:
            if decision.get("is_manual"):
                new_percepts = env.get_percepts(new_pos)
                p_msgs = []
                if "Breeze" in new_percepts: p_msgs.append("breeze detected")
                if "Stench" in new_percepts: p_msgs.append("stench detected")
                if p_msgs:
                    decision["result_text"] = f"Safe move. {', '.join(p_msgs).capitalize()}."
                else:
                    decision["result_text"] = "Safe move. No hazards nearby."
            
    # Process grab (auto-grab in manual if on gold)
    if (action == "GRAB" or manual_direction) and env.grid[env.agent_pos]["gold"] and env.agent_alive:
        env.grid[env.agent_pos]["gold"] = False
        env.agent_has_gold = True
        game["score"] += SCORE_GOLD
        env.agent_escaped = True
        decision["reason"] += " (VICTORY)"
        decision["explanation"] += " Secured the gold!"
        if decision.get("is_manual"):
            decision["result_text"] = "You found the gold! You win!"
            
    return jsonify({
        "status": "success",
        "decision": decision,
        "score": game["score"]
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
