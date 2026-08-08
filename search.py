from collections import deque
import heapq

def bfs_path(start, target, safe_cells, get_adjacent):
    """
    Finds shortest path from start to target through safe_cells using BFS.
    Returns list of moves (dx, dy) or None.
    """
    if start == target:
        return []
        
    queue = deque([(start, [])])
    visited = {start}
    
    while queue:
        current, path = queue.popleft()
        
        for adj in get_adjacent(current):
            if adj == target:
                return path + [adj]
            if adj in safe_cells and adj not in visited:
                visited.add(adj)
                queue.append((adj, path + [adj]))
                
    return None

def astar_path(start, target, safe_cells, get_adjacent):
    """
    Finds shortest path from start to target through safe_cells using A* 
    with Manhattan distance heuristic.
    Returns list of moves (dx, dy) or None.
    """
    def manhattan(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    if start == target:
        return []

    # Priority queue: (f_score, g_score, current_pos, path)
    queue = [(manhattan(start, target), 0, start, [])]
    visited = {start: 0} # pos -> g_score

    while queue:
        f, g, current, path = heapq.heappop(queue)

        if current == target:
            return path

        for adj in get_adjacent(current):
            # We can step into target even if it's not strictly 'safe' (e.g. going in for the kill or risky guess)
            if adj == target or adj in safe_cells:
                new_g = g + 1
                if adj not in visited or new_g < visited[adj]:
                    visited[adj] = new_g
                    f_score = new_g + manhattan(adj, target)
                    heapq.heappush(queue, (f_score, new_g, adj, path + [adj]))

    return None

def convert_path_to_actions(current_pos, current_dir, path):
    """
    Converts a sequence of coordinates into agent actions:
    FORWARD, TURN_LEFT, TURN_RIGHT.
    Directions: 0: Right (1,0), 1: Up (0,1), 2: Left (-1,0), 3: Down (0,-1)
    """
    actions = []
    curr_p = current_pos
    curr_d = current_dir
    
    for next_p in path:
        dx = next_p[0] - curr_p[0]
        dy = next_p[1] - curr_p[1]
        
        target_dir = None
        if dx == 1: target_dir = 0
        elif dy == 1: target_dir = 1
        elif dx == -1: target_dir = 2
        elif dy == -1: target_dir = 3
        
        # Calculate turns
        diff = (target_dir - curr_d) % 4
        if diff == 1:
            actions.append("TURN_LEFT")
        elif diff == 2:
            actions.append("TURN_LEFT")
            actions.append("TURN_LEFT")
        elif diff == 3:
            actions.append("TURN_RIGHT")
            
        actions.append("FORWARD")
        curr_p = next_p
        curr_d = target_dir
        
    return actions, curr_d
