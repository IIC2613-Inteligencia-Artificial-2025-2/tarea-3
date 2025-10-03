from collections import deque
import time

class BFS:
    def __init__(self, robot):
        self.robot = robot
        self.exp = 0

    def search(self, initial_state, goal_state):
        t = time.process_time()
        queue = deque([initial_state])
        visited = {initial_state}
        parent = {initial_state: None}

        while queue:
            actual_state = queue.popleft()
            self.exp += 1

            for succ in self.robot.succ(actual_state):
                if succ not in visited and not self.robot.check_collisions(actual_state, succ):
                    if self.robot.is_goal(succ, goal_state):
                        parent[succ] = actual_state
                        camino = self.__reconstruir_camino(parent, succ)
                        return camino, self.exp, time.process_time() - t
                    
                    visited.add(succ)
                    parent[succ] = actual_state
                    queue.append(succ)

        return None, self.exp, time.process_time() - t

    def __reconstruir_camino(self, parent, meta):
        camino = []
        estado = meta
        while estado is not None:
            camino.append(estado)
            estado = parent[estado]
        camino.reverse()
        return camino

