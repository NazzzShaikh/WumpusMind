import random
from search import bfs_path, astar_path, convert_path_to_actions

class RandomAgent:
    def __init__(self, size):
        self.pos = (0, 0)
        self.dir = 0
        
    def get_action(self, percepts):
        # Pure random walk
        actions = ["FORWARD", "TURN_LEFT", "TURN_RIGHT"]
        act = random.choice(actions)
        return {
            "action": act,
            "target": list(self.pos),
            "reason": "Random Walk",
            "explanation": "Randomly picked an action.",
            "confidence": 0.33
        }

    def update_agent_state(self, action):
        if action == "TURN_LEFT":
            self.dir = (self.dir + 1) % 4
        elif action == "TURN_RIGHT":
            self.dir = (self.dir - 1) % 4
        elif action == "FORWARD":
            dx, dy = 0, 0
            if self.dir == 0: dx = 1
            elif self.dir == 1: dy = 1
            elif self.dir == 2: dx = -1
            elif self.dir == 3: dy = -1
            self.pos = (self.pos[0] + dx, self.pos[1] + dy)

class BFSAgent(RandomAgent):
    def __init__(self, size):
        super().__init__(size)
        self.size = size
        self.visited = set()
        self.action_queue = []
        
    def get_action(self, percepts):
        self.visited.add(self.pos)
        
        if self.action_queue:
            return {
                "action": self.action_queue.pop(0),
                "target": list(self.pos),
                "reason": "BFS",
                "explanation": "Following BFS path.",
                "confidence": 1.0
            }
            
        # Find unvisited neighbors to explore using BFS
        # For a pure BFS agent, it doesn't know what's safe. It just explores blindly.
        queue = [(self.pos, [])]
        bfs_visited = {self.pos}
        
        target = None
        best_path = None
        
        while queue:
            curr, path = queue.pop(0)
            
            # If we found an unvisited cell, path to it
            if curr not in self.visited:
                target = curr
                best_path = path
                break
                
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = curr[0] + dx, curr[1] + dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    if (nx, ny) not in bfs_visited:
                        bfs_visited.add((nx, ny))
                        queue.append(((nx, ny), path + [(nx, ny)]))
                        
        if best_path:
            actions, _ = convert_path_to_actions(self.pos, self.dir, best_path)
            self.action_queue = actions[1:]
            return {
                "action": actions[0],
                "target": list(target),
                "reason": "BFS",
                "explanation": "Exploring nearest unvisited cell (blindly).",
                "confidence": 1.0
            }
            
        return super().get_action(percepts) # Fallback to random


class AStarAgent(RandomAgent):
    def __init__(self, size):
        super().__init__(size)
        self.size = size
        self.visited = set()
        self.action_queue = []
        
    def get_action(self, percepts):
        self.visited.add(self.pos)
        
        if self.action_queue:
            return {
                "action": self.action_queue.pop(0),
                "target": list(self.pos),
                "reason": "A*",
                "explanation": "Following A* path.",
                "confidence": 1.0
            }
            
        # Find unvisited neighbors using A* distance
        # A pure A* agent explores blindly but evaluates paths based on Manhattan distance
        # We can reuse the BFS frontier logic but sort by astar path length
        queue = [(self.pos, [])]
        bfs_visited = {self.pos}
        
        candidates = []
        
        while queue:
            curr, path = queue.pop(0)
            
            if curr not in self.visited:
                candidates.append((curr, path))
                
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = curr[0] + dx, curr[1] + dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    if (nx, ny) not in bfs_visited:
                        bfs_visited.add((nx, ny))
                        queue.append(((nx, ny), path + [(nx, ny)]))
                        
        if candidates:
            # Sort candidates by Manhattan distance from current position as the heuristic
            candidates.sort(key=lambda c: abs(c[0][0] - self.pos[0]) + abs(c[0][1] - self.pos[1]))
            target, best_path = candidates[0]
            
            actions, _ = convert_path_to_actions(self.pos, self.dir, best_path)
            self.action_queue = actions[1:]
            return {
                "action": actions[0],
                "target": list(target),
                "reason": "A*",
                "explanation": "Exploring unvisited cell using A*.",
                "confidence": 1.0
            }
            
        return super().get_action(percepts) # Fallback to random
