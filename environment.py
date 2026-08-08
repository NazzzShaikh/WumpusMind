import random
from config import DIFFICULTY_PRESETS

class WumpusEnvironment:
    def __init__(self, size=4, difficulty="Easy"):
        self.size = size
        self.difficulty = difficulty
        self.grid = {}  # (x, y) -> {"wumpus": bool, "pit": bool, "gold": bool}
        self.agent_pos = (0, 0)
        self.agent_dir = 0  # 0: Right, 1: Up, 2: Left, 3: Down
        self.agent_alive = True
        self.agent_has_gold = False
        self.agent_escaped = False
        self.agent_has_arrow = True
        self.wumpus_alive = {} # (x, y) -> bool
        
        self._generate_grid()

    def _generate_grid(self):
        # Initialize empty grid
        for x in range(self.size):
            for y in range(self.size):
                self.grid[(x, y)] = {"wumpus": False, "pit": False, "gold": False}
        
        cfg = DIFFICULTY_PRESETS.get(self.difficulty, DIFFICULTY_PRESETS["Easy"])
        pit_prob = cfg["pit_prob"]
        wumpus_count = cfg["wumpus_count"]
        
        # Place Pits
        for x in range(self.size):
            for y in range(self.size):
                if (x, y) != (0, 0) and random.random() < pit_prob:
                    self.grid[(x, y)]["pit"] = True
                    
        # Place Wumpus(es)
        available_cells = [(x, y) for x in range(self.size) for y in range(self.size) if (x, y) != (0, 0)]
        for _ in range(wumpus_count):
            if not available_cells:
                break
            wx, wy = random.choice(available_cells)
            self.grid[(wx, wy)]["wumpus"] = True
            self.wumpus_alive[(wx, wy)] = True
            if not cfg["allow_multiple_wumpus"]:
                available_cells.remove((wx, wy))

        # Place Gold
        gold_cells = [(x, y) for x in range(self.size) for y in range(self.size) if (x, y) != (0, 0) and not self.grid[(x, y)]["pit"] and not self.grid[(x, y)]["wumpus"]]
        if not gold_cells: # fallback if all non-start cells are hazards
            gold_cells = [(x, y) for x in range(self.size) for y in range(self.size) if (x, y) != (0, 0)]
        
        if gold_cells:
            gx, gy = random.choice(gold_cells)
            self.grid[(gx, gy)]["gold"] = True

    def get_percepts(self, pos=None):
        if pos is None:
            pos = self.agent_pos
        x, y = pos
        percepts = {"breeze": False, "stench": False, "glitter": False, "bump": False, "scream": False}
        
        if self.grid[pos]["gold"]:
            percepts["glitter"] = True
            
        for nx, ny in self._get_adjacent(pos):
            if self.grid[(nx, ny)]["pit"]:
                percepts["breeze"] = True
            if self.grid[(nx, ny)]["wumpus"]:
                percepts["stench"] = True
                
        return percepts

    def _get_adjacent(self, pos):
        x, y = pos
        adj = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                adj.append((nx, ny))
        return adj

    def is_valid_pos(self, pos):
        x, y = pos
        return 0 <= x < self.size and 0 <= y < self.size
    
    def step(self, action):
        """
        Actions: 'FORWARD', 'TURN_LEFT', 'TURN_RIGHT', 'GRAB', 'CLIMB', 'SHOOT'
        Returns: (percepts, reward, done, info)
        """
        # (This will be called by the game engine, not necessarily the agent directly, 
        # but useful for simulation)
        pass # We'll implement actual game step logic in a central game controller or within the agent orchestrator

    def get_state_dict(self):
        # Returns a serializeable dictionary of the true environment state
        return {
            "size": self.size,
            "grid": [{"x": x, "y": y, **self.grid[(x, y)]} for x, y in self.grid],
            "agent_pos": self.agent_pos,
            "agent_dir": self.agent_dir,
            "agent_alive": self.agent_alive,
            "agent_has_gold": self.agent_has_gold,
            "agent_escaped": self.agent_escaped,
            "wumpus_alive": [{"x": x, "y": y, "alive": self.wumpus_alive[(x, y)]} for x, y in self.wumpus_alive]
        }
