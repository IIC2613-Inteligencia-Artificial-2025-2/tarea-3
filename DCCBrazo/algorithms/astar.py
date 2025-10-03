from algorithms.node import Node
from algorithms.binary_heap import BinaryHeap
from trig import heuristic_trig
from consts import L1, L2
import time

class AStar:
    def __init__(self, robot, heuristic = heuristic_trig, weight = 1.0):
        self.robot = robot
        self.h = heuristic
        self.weight = weight

    def _f(self, g, h):
        return g + self.weight*h         

    def search(self, start_state, goal):
        t = time.process_time()
        self.open = BinaryHeap()
        self.generated = {} 
        self.best_g = {} 
        self.closed = set()
        self.expansions = 0

        n0 = Node(start_state)
        n0.g = 0
        n0.h = self.h(start_state, goal, L1, L2)
        n0.key = self._f(n0.g, n0.h)
        self.open.insert(n0)
        self.generated[start_state] = n0
        self.best_g[start_state] = 0

        while not self.open.is_empty():
            n = self.open.extract()
            s = n.state
            if s in self.closed:
                continue
            self.closed.add(s)

            if self.robot.is_goal(s, goal):
                return self._reconstruct_path(n), self.expansions, time.process_time() - t

            self.expansions += 1
            for s2 in self.robot.succ(s):
                if self.robot.check_collisions(s, s2):
                    continue
                g2 = n.g + 1
                if s2 in self.closed and g2 >= self.best_g.get(s2, float("inf")):
                    continue

                m = self.generated.get(s2)
                if m is None:
                    m = Node(s2)
                    m.h = self.h(s2, goal, L1, L2)
                    self.generated[s2] = m

                if g2 < self.best_g.get(s2, float("inf")):
                    self.best_g[s2] = g2
                    m.parent = n
                    m.g = g2
                    m.key = self._f(m.g, m.h)
                    self.open.insert(m) 

        return None, self.expansions, time.process_time() - t

    def _reconstruct_path(self, node):
        path = []
        while node:
            path.append(node.state)
            node = node.parent
        return list(reversed(path))
