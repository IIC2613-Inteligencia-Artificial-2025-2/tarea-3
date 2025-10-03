from trig import heuristic_trig
from consts import L1, L2
import math

initial = (0, math.pi)

def check_heuristic_trig(initial, goal, L1, L2, correct_h):
    your_h = heuristic_trig(initial, goal, L1, L2)
    if your_h == correct_h:
        return "PASS"
    answer = f"correct answer: {correct_h}\nyour answer: {your_h}"
    return "FAIL\n" + answer

print("TEST 1:")
goal = (0, 320)
test_1 = check_heuristic_trig(initial, goal, L1, L2, 16)
print(test_1)
print()

print("TEST 2:")
goal = (120, 200)
test_2 = check_heuristic_trig(initial, goal, L1, L2, 16)
print(test_2)
print()

print("TEST 3:")
goal = (60*math.sqrt(2) + 200, 60*math.sqrt(2))
test_3 = check_heuristic_trig(initial, goal, L1, L2, 8)
print(test_3)