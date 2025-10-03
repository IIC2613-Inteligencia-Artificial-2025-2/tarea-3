from trig import ang_to_cart
import math

def check_test_ang_to_cart(theta1, theta2, L1, L2, tuple1, tuple2):
    tuple1_test, tuple2_test = ang_to_cart(theta1, theta2, L1, L2)
    if round(tuple1_test[0], 1) == round(tuple1[0], 1):
        if round(tuple1_test[1], 1) == round(tuple1[1], 1):
            if round(tuple2_test[0], 1) == round(tuple2[0], 1):
                if round(tuple2_test[1], 1) == round(tuple2[1], 1):
                    return "PASS"
    
    answer = f"correct answer: {tuple1}, {tuple2}\nyour answer: {tuple1_test}, {tuple2_test}"
    return "FAIL\n" + answer

print("TEST 1:")
L1, L2 = 100, 200
theta1, theta2 = math.pi/4, math.pi/2

test_1 = check_test_ang_to_cart(theta1, theta2, L1, L2, (50*math.sqrt(2), 50*math.sqrt(2)), (150*math.sqrt(2), -50*math.sqrt(2)))
print(test_1)
print()

print("TEST 2:")
L1, L2 = 120, 200
theta1, theta2 = math.pi/2, math.pi/3

test_2 = check_test_ang_to_cart(theta1, theta2, L1, L2, (0, 120), (100*math.sqrt(3), 20))
print(test_2)
print()

print("TEST 3:")
L1, L2 = 100, 50
theta1, theta2 = 2*math.pi/3, math.pi/6

test_3 = check_test_ang_to_cart(theta1, theta2, L1, L2, (-50, 50*math.sqrt(3)), (-50 + 25*math.sqrt(3), 50*math.sqrt(3) - 25))
print(test_3)