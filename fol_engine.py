class FOLEngine:
    def __init__(self, kb):
        self.kb = kb
        self.size = kb.size

    def _get_adjacent(self, pos):
        return self.kb._get_adjacent(pos)

    def resolve_wumpus(self):
        """
        Attempts to use First-Order Logic style resolution based on known stenches
        to pinpoint the Wumpus. Returns (wumpus_pos, reasoning_string) if found, else (None, None).
        
        Example Rule: Wumpus must be in intersection of adjacent unvisited cells of all known stenches.
        If a stench has only one adjacent non-safe cell, that cell MUST be the Wumpus.
        """
        reasoning = []
        possible_wumpus_cells_per_stench = []
        
        for stench_pos in self.kb.stenches:
            adj = self._get_adjacent(stench_pos)
            # Wumpus must be in an adjacent cell that is NOT known to be no_wumpus
            possible_cells = set(adj) - self.kb.no_wumpus
            
            if len(possible_cells) == 1:
                w_pos = possible_cells.pop()
                self.kb.wumpus.add(w_pos)
                reasoning_str = f"FOL Resolution: Stench at {stench_pos} has only one possible adjacent cell for Wumpus -> {w_pos}."
                return w_pos, reasoning_str
                
            possible_wumpus_cells_per_stench.append(possible_cells)
            
        # Intersect all possible cells from different stenches
        if possible_wumpus_cells_per_stench:
            intersection = set.intersection(*possible_wumpus_cells_per_stench)
            if len(intersection) == 1:
                w_pos = intersection.pop()
                self.kb.wumpus.add(w_pos)
                reasoning_str = f"FOL Resolution: Intersecting stenches confirmed Wumpus must be at {w_pos}."
                return w_pos, reasoning_str
                
        return None, None
