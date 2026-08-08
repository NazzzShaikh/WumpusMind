import json
import re

# Parse agent.js to see what the exact strings are
with open("static/js/agent.js", "r") as f:
    content = f.read()

# Look for the exact icon logic in fetchState
if "sprite.innerHTML =" in content:
    idx = content.find("if (!env.agent_alive)")
    if idx != -1:
        print("Found agent_alive check!")
        print(content[idx:idx+800])
    else:
        print("Could not find agent_alive check!")
