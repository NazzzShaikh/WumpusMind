from knowledge_base import KnowledgeBase
from fol_engine import FOLEngine
from probability_engine import ProbabilityEngine
from search import astar_path, convert_path_to_actions

class HybridAgent:
    def __init__(self, size, pit_prob, wumpus_count=1):
        self.kb = KnowledgeBase(size)
        self.fol = FOLEngine(self.kb)
        self.prob = ProbabilityEngine(self.kb, pit_prob, wumpus_count)
        
        self.pos = (0, 0)
        self.dir = 0
        self.has_arrow = True
        self.action_queue = []
        
    def get_action(self, percepts):
        """
        Main decision loop.
        Returns: {"action": str, "target": [x,y], "reason": str, "explanation": str, "confidence": float}
        """
        # If we have actions queued up (from a path), execute them
        if self.action_queue:
            act = self.action_queue.pop(0)
            return {
                "action": act, 
                "target": list(self.pos), # Target isn't perfectly represented here, it's a step
                "reason": "Search", 
                "explanation": "Executing planned path.", 
                "confidence": 1.0
            }

        # 1. Update KB with current percepts
        kb_reasoning = self.kb.add_percepts(self.pos, percepts)
        
        # Check if we should grab gold
        if percepts.get("glitter"):
            return {
                "action": "GRAB",
                "target": list(self.pos),
                "reason": "Reflex",
                "explanation": "Glitter detected! Grabbing the gold.",
                "confidence": 1.0
            }
            
        # 2. Try to find Wumpus with FOL if we have arrow and stenches
        if self.has_arrow and self.kb.stenches:
            w_pos, fol_reason = self.fol.resolve_wumpus()
            if w_pos:
                # Need to face Wumpus and shoot. For simplicity in pathing, 
                # let's just say we move to adjacent and shoot. 
                # Or just turn if adjacent.
                pass # Skipping full shoot logic for now, but framework is here
                
        # 3. Find safe unvisited cells (Frontier)
        frontier = self.kb.get_frontier()
        if frontier:
            # Pick the closest safe cell using A*
            best_path = None
            best_target = None
            min_len = float('inf')
            
            for target in frontier:
                path = astar_path(self.pos, target, self.kb.safe, self.kb._get_adjacent)
                if path and len(path) < min_len:
                    min_len = len(path)
                    best_path = path
                    best_target = target
                    
            if best_path:
                actions, _ = convert_path_to_actions(self.pos, self.dir, best_path)
                self.action_queue = actions[1:] # Store subsequent actions
                return {
                    "action": actions[0],
                    "target": list(best_target),
                    "reason": "KB + A*",
                    "explanation": f"Cell {best_target} is 100% safe. Routing there.",
                    "confidence": 1.0
                }

        # 4. If no guaranteed safe cells, use Probability Engine
        best_guess, prob_reason, conf = self.prob.get_best_guess()
        if best_guess:
            path = astar_path(self.pos, best_guess, self.kb.safe, self.kb._get_adjacent)
            if path:
                actions, _ = convert_path_to_actions(self.pos, self.dir, path)
                self.action_queue = actions[1:]
                return {
                    "action": actions[0],
                    "target": list(best_guess),
                    "reason": "Probability + A*",
                    "explanation": prob_reason,
                    "confidence": conf
                }
                
        # 5. Fallback - random valid move (should rarely happen if probabilities cover everything)
        import random
        fallback_action = random.choice(["FORWARD", "TURN_LEFT", "TURN_RIGHT"])
        return {
            "action": fallback_action,
            "target": list(self.pos),
            "reason": "Fallback",
            "explanation": "No logical moves found.",
            "confidence": 0.0
        }

    def update_agent_state(self, action):
        """Updates internal pos/dir based on action taken (assuming success)"""
        if action == "TURN_LEFT":
            self.dir = (self.dir + 1) % 4
        elif action == "TURN_RIGHT":
            self.dir = (self.dir - 1) % 4
        elif action == "FORWARD":
            dx, dy = 0, 0
            if self.dir == 0: dx = 1
            elif self.dir == 1: dy = 1
            elif self.dir == 2: dx = -1
            elif self.dir == 3: dy = -1
            self.pos = (self.pos[0] + dx, self.pos[1] + dy)
