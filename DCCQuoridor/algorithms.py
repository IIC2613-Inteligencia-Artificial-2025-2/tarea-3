# NO TOCAR

from collections import deque
import heapq
from board import MOVES

NOT_FOUND = 9999

def bfs_to_goal_row(game, start_rc, goal_row):
    (sr, sc) = start_rc
    size = game.board.size
    visited = [[-1] * size for _ in range(size)]
    dq = deque([(sr, sc)])
    visited[sr][sc] = 0

    while dq:
        r, c = dq.popleft()
        if r == goal_row:
            return True, visited[r][c]
        for dr, dc in MOVES:
            if game.is_open(r, c, (dr, dc)):
                nr, nc = r + dr, c + dc
                if visited[nr][nc] == -1:
                    visited[nr][nc] = visited[r][c] + 1
                    dq.append((nr, nc))
    return False, NOT_FOUND

def astar_to_goal_row(game, start_rc, goal_row):
    (sr, sc) = start_rc
    size = game.board.size

    def heuristic(r, _c):
        return abs(goal_row - r)
    
    INF = 10**9
    gbest = [[INF] * size for _ in range(size)]
    pq = []

    gbest[sr][sc] = 0
    heapq.heappush(pq, (heuristic(sr, sc), 0, sr, sc))
    while pq:
        f, g, r, c = heapq.heappop(pq)
        if r == goal_row:
            return True, g
        if g != gbest[r][c]:
            continue
        for dr, dc in MOVES:
            if game.is_open(r, c, (dr, dc)):
                nr, nc = r + dr, c + dc
                ng = g + 1
                if ng < gbest[nr][nc]:
                    gbest[nr][nc] = ng
                    heapq.heappush(pq, (ng + heuristic(nr, nc), ng, nr, nc))
    return False, NOT_FOUND
