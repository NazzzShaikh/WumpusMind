import requests

s = requests.Session()
# Start game
resp = s.post("http://localhost:5000/api/setup", json={
    "size": 4,
    "difficulty": "Hard",
    "algorithm": "Hybrid",
    "play_mode": "autoplay"
})
print("Setup:", resp.json())

# Step until game over
dead_or_escaped = False
for i in range(50):
    resp = s.post("http://localhost:5000/api/step", json={"manual_direction": None})
    data = resp.json()
    if data.get("status") == "game_over":
        print("Game was already over.")
        break
    
    decision = data.get("decision", {})
    reason = decision.get("reason", "")
    print(f"Step {i+1}: {reason}")
    if "(DEATH)" in reason or "(VICTORY)" in reason:
        dead_or_escaped = True
        break

# Fetch state
resp = s.get("http://localhost:5000/api/state")
state = resp.json()
print("Alive:", state["env"]["agent_alive"])
print("Escaped:", state["env"]["agent_escaped"])

