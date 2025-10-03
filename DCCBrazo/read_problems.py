def read_problem(filename):
    file = open(filename, "r")
    lines = file.readlines()
    GOAL_1 = read_tuple(lines[0])
    GOAL_2 = read_tuple(lines[1])
    OBS_POS = []
    if "obs" in filename:
        n = len(lines) - 2
        for i in range(n):
            OBS_POS.append(read_tuple(lines[2 + i]))
    return GOAL_1, GOAL_2, OBS_POS

def read_tuple(line):
    goal_line = line.strip("\n").split(",")
    goal = (float(goal_line[0]), float(goal_line[1]))
    return goal