import math
from trig import ang_to_cart
from consts import WIDTH, HEIGHT, L1, L2

class RobotState:
    def __init__(self, L1, L2, OBSTACLES):
        self.L1 = L1
        self.L2 = L2
        self.OBSTACLES = OBSTACLES

    def succ(self, state):
        theta1, theta2 = state
        delta = 0.1
        return [(theta1 - delta, theta2 - delta),
                (theta1 + delta, theta2 - delta),
                (theta1 - delta, theta2 + delta),
                (theta1 + delta, theta2 + delta),
                (theta1 - delta, theta2),
                (theta1 + delta, theta2),
                (theta1, theta2 - delta),
                (theta1, theta2 + delta)]

    def is_goal(self, state, goal, error=8):
        theta1, theta2 = state
        x_goal, y_goal = goal
        x, y = ang_to_cart(theta1, theta2, L1, L2)[1]
        return (x-x_goal)**2 + (y-y_goal)**2 <= error**2
    
    def check_collisions(self, state, next_state, steps=10):
        theta1, theta2 = state
        theta1_next, theta2_next = next_state

        for i in range(steps+1):
            # Interpolación lineal de ángulos
            t = i / steps
            th1 = theta1 + t * (theta1_next - theta1)
            th2 = theta2 + t * (theta2_next - theta2)

            # Posiciones del brazo
            (x1, y1), (x2, y2) = ang_to_cart(th1, th2, self.L1, self.L2)
            cx, cy = WIDTH // 2, HEIGHT // 2
            brazo_1_start = (cx, cy)
            brazo_1_end   = (cx + x1, cy - y1)
            brazo_2_start = brazo_1_end
            brazo_2_end   = (cx + x2, cy - y2)

            # Revisar contra todos los obstáculos
            for ob in self.OBSTACLES:
                if (self.check_collision_segment(brazo_1_start, brazo_1_end, ob.position, ob.radius) or
                    self.check_collision_segment(brazo_2_start, brazo_2_end, ob.position, ob.radius)):
                    return True
        return False
    
    def interpolate_states(state1, state2, steps=10):
        theta1_a, theta2_a = state1
        theta1_b, theta2_b = state2
        for i in range(steps+1):
            t = i / steps
            yield (
                theta1_a + t * (theta1_b - theta1_a),
                theta2_a + t * (theta2_b - theta2_a)
            )

    def check_collision_segment(self, p1, p2, center, radius):
        # Vector del segmento
        x1, y1 = p1
        x2, y2 = p2
        cx, cy = center

        # Vector del segmento y del centro al inicio
        dx, dy = x2 - x1, y2 - y1
        fx, fy = cx - x1, cy - y1

        # Proyección del vector centro-inicio sobre el segmento (normalizada)
        t = (fx*dx + fy*dy) / float(dx*dx + dy*dy)

        # Limitar t a [0,1] para que caiga en el segmento
        t = max(0, min(1, t))

        # Punto más cercano en el segmento
        closest_x = x1 + t*dx
        closest_y = y1 + t*dy

        # Distancia del círculo al punto más cercano
        dist_sq = (closest_x - cx)**2 + (closest_y - cy)**2
        
        safety_margin = 5  # píxeles extra
        return dist_sq <= (radius + safety_margin)**2


    