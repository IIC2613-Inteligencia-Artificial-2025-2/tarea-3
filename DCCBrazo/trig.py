import math

def ang_to_cart(theta1: float, theta2: float, L1: float, L2: float):
    # TODO: Actividad 1
    pass

def heuristic_trig(state, goal, L1, L2):
    # TODO: Actividad 1
    pass

def normalize_angle(angle):
    if angle < 0:
        return 2*math.pi + angle
    elif angle >= 2*math.pi:
        return angle - 2*math.pi
    return angle

def angle_dist(a, b):
    diff = (a - b + math.pi) % (2 * math.pi) - math.pi
    return abs(diff)