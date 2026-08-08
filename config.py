# config.py

DIFFICULTY_PRESETS = {
    "Easy": {
        "pit_prob": 0.1,
        "wumpus_count": 1,
        "allow_multiple_wumpus": False
    },
    "Medium": {
        "pit_prob": 0.15,
        "wumpus_count": 1,
        "allow_multiple_wumpus": False
    },
    "Hard": {
        "pit_prob": 0.2,
        "wumpus_count": 2,
        "allow_multiple_wumpus": True
    }
}

SCORE_MOVE = -1
SCORE_ARROW = -10
SCORE_GOLD = 1000
SCORE_DEATH = -10000

# Wumpus World cells are usually represented as (x, y) where x is col (1 to N) and y is row (1 to N).
# Bottom-left is often (1, 1). We'll stick to a 0-indexed internal representation (0 to N-1),
# but external (UI/logging) can use 1-indexed.
