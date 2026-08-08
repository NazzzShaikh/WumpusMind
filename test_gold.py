import sys
from environment import WumpusEnvironment

wumpus_gold_count = 0
for _ in range(100):
    env = WumpusEnvironment(size=4, difficulty="Easy")
    for x in range(4):
        for y in range(4):
            if env.grid[(x, y)]["gold"]:
                if env.grid[(x, y)]["wumpus"]:
                    wumpus_gold_count += 1
print(f"Gold on Wumpus in {wumpus_gold_count}/100 games")
