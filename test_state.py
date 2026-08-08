import requests

s = requests.Session()
s.post("http://localhost:5000/api/setup", json={
    "size": 4,
    "difficulty": "Easy",
    "algorithm": "Hybrid",
    "play_mode": "manual"
})

resp = s.get("http://localhost:5000/api/state")
data = resp.json()
print("Risks present:", "risks" in data["agent"])
if "risks" in data["agent"]:
    print("Risks length:", len(data["agent"]["risks"]))
