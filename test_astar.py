import requests

s = requests.Session()
# Start game with Pure A*
resp = s.post("http://localhost:5000/api/setup", json={
    "size": 4,
    "difficulty": "Easy",
    "algorithm": "AStar",
    "play_mode": "autoplay"
})
print("Setup AStar:", resp.json())

for i in range(20):
    resp = s.post("http://localhost:5000/api/step", json={"manual_direction": None})
    if resp.status_code != 200:
        print("Error!", resp.text)
        break
    data = resp.json()
    if data.get("status") == "game_over":
        print("Game Over gracefully.")
        break
    
    decision = data.get("decision", {})
    print(f"Step {i+1}: {decision.get('action')} - {decision.get('reason')}")
