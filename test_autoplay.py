import requests
import json

s = requests.Session()
def play_game(algo):
    resp = s.post("http://localhost:5000/api/setup", json={
        "size": 4,
        "difficulty": "Easy",
        "algorithm": algo,
        "play_mode": "autoplay"
    })
    for i in range(100):
        resp = s.post("http://localhost:5000/api/step", json={"manual_direction": None})
        if resp.status_code != 200:
            return "ERROR"
        data = resp.json()
        if data.get("status") == "game_over":
            return "GAME_OVER"
        decision = data.get("decision", {})
        if "(DEATH)" in decision.get("reason", "") or "(VICTORY)" in decision.get("reason", ""):
            # next step should return game_over
            pass
    return "STUCK"

results = {"AStar": [], "Hybrid": []}
for algo in ["AStar", "Hybrid"]:
    for _ in range(10):
        results[algo].append(play_game(algo))

print(json.dumps(results, indent=2))
