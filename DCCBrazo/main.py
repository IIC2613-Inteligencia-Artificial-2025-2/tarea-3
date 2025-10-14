from obstacles import create_obstacles
from arm_viewer import ArmViewer
from robot import RobotState
from algorithms.bfs import BFS
from algorithms.astar import AStar
from algorithms.ara import ARA
from read_problems import read_problem
import sys
import math
from consts import R_MESA, OBS_RADIUS, L1, L2

n_problem = sys.argv[1]
alg_name = sys.argv[2]
obstacles = sys.argv[3]

if obstacles == "True":
    name_problem = f"problems/problem_{n_problem}_obs.txt"
else:
    name_problem = f"problems/problem_{n_problem}.txt"

GOAL_1, GOAL_2, OBS_POS = read_problem(name_problem)
obs_info = create_obstacles(OBS_POS, OBS_RADIUS)
robot = RobotState(L1, L2, obs_info)

if alg_name == "astar":
    alg = AStar(robot, weight=1)    # TODO: Cambiar weight para actividad 4
elif alg_name == "bfs":
    alg = BFS(robot)
elif alg_name == "ara":
    alg = ARA(robot)
elif alg_name == "zero":
    alg = AStar(robot, lambda state, goal, L1, L2: 0)


search_1 = alg.search((0, math.pi), GOAL_1)
search_1_path, search_1_exp, search_1_time = search_1

search_2 = alg.search(search_1_path[-1], GOAL_2)
search_2_path, search_2_exp, search_2_time = search_2

total_exp = search_1_exp + search_2_exp
total_time = search_1_time + search_2_time
path_len = len(search_1_path) + len(search_2_path)

print(f"ALGORITHM  : {alg_name}")
print(f"EXP        : {total_exp}")
print(f"TIME (s)   : {total_time}")
print(f"PATH LENGHT: {path_len}")

arm_viewer = ArmViewer(robot, search_1_path, search_2_path, GOAL_1, GOAL_2, R_MESA, obs_info)
arm_viewer.run()