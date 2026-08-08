class KnowledgeBase:
    def __init__(self, size):
        self.size = size
        self.visited = set()
        self.safe = set()
        self.pits = set()
        self.wumpus = set()
        self.breezes = set()
        self.stenches = set()
        self.no_pits = set()
        self.no_wumpus = set()
        
        # Start is always safe
        self.mark_safe((0, 0))

    def _get_adjacent(self, pos):
        x, y = pos
        adj = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                adj.append((nx, ny))
        return adj

    def mark_safe(self, pos):
        if pos not in self.safe:
            self.safe.add(pos)
            self.no_pits.add(pos)
            self.no_wumpus.add(pos)
            if pos in self.pits: self.pits.remove(pos)
            if pos in self.wumpus: self.wumpus.remove(pos)

    def add_percepts(self, pos, percepts):
        """
        Updates the KB with new percepts from a visited cell.
        Returns a list of reasoning strings.
        """
        self.visited.add(pos)
        self.mark_safe(pos)
        
        reasoning = []
        
        # Forward Chaining for Pits
        if percepts.get("breeze"):
            self.breezes.add(pos)
        else:
            # Not breeze -> all adjacent are not pits
            for adj in self._get_adjacent(pos):
                if adj not in self.no_pits:
                    self.no_pits.add(adj)
                    if adj in self.pits: self.pits.remove(adj)
                    reasoning.append(f"No breeze at {pos}, so {adj} has no Pit.")
                    
        # Forward Chaining for Wumpus
        if percepts.get("stench"):
            self.stenches.add(pos)
        else:
            # Not stench -> all adjacent are not wumpus
            for adj in self._get_adjacent(pos):
                if adj not in self.no_wumpus:
                    self.no_wumpus.add(adj)
                    if adj in self.wumpus: self.wumpus.remove(adj)
                    reasoning.append(f"No stench at {pos}, so {adj} has no Wumpus.")
                    
        # Conclude safe cells (no pit AND no wumpus)
        for x in range(self.size):
            for y in range(self.size):
                p = (x, y)
                if p not in self.safe and p in self.no_pits and p in self.no_wumpus:
                    self.mark_safe(p)
                    reasoning.append(f"{p} is proven safe (No Pit & No Wumpus).")
                    
        return reasoning
        
    def get_frontier(self):
        """Returns cells that are safe but not yet visited."""
        return list(self.safe - self.visited)
