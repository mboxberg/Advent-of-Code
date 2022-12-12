import numpy as np

parttwo = True
elevation_map = list()
start_line = 0

moves = {(1, 0): ">", (-1, 0): "<", (0, 1): "v", (0, -1): "^"}

with open("../dat/12") as input_file:
    y_max = 0
    while True:
        line = input_file.readline()
        if not line:
            break
        elevation_line = list(line[:-1])
        if "S" in elevation_line:
            y_start = y_max
            x_start = elevation_line.index("S")
        if "E" in elevation_line:
            y_end = y_max
            x_end = elevation_line.index("E")
        elevation_map.append(list(line[:-1]))
        y_max += 1
    x_max = len(elevation_line)

graph = {}
for y in range(y_max):
    for x in range(x_max):
        neighbors = []
        if elevation_map[y][x] == "S":
            current_elevation = ord("a")
        elif elevation_map[y][x] == "E":
            current_elevation = ord("z")
        else:
            current_elevation = ord(elevation_map[y][x])
        for test in moves.keys():
            x_test = x + test[0]
            y_test = y + test[1]
            if x_test < 0 or y_test < 0 or x_test >= x_max or y_test >= y_max:
                continue
            if elevation_map[y_test][x_test] == "S":
                test_elevation = ord("a")
            elif elevation_map[y_test][x_test] == "E":
                test_elevation = ord("z")
            else:
                test_elevation = ord(elevation_map[y_test][x_test])
            if parttwo and elevation_map[y_test][x_test] == "a":
                neighbors.append(((x_test, y_test), 0))
            else:
                neighbors.append(((x_test, y_test), 1 if test_elevation <= current_elevation + 1 else np.Inf))
        graph[(x, y)] = neighbors

number_of_steps = [[np.Inf for _ in range(x_max)] for _ in range(y_max)]
number_of_steps[y_start][x_start] = 0

visited = [[False for _ in range(x_max)] for _ in range(y_max)]

for _ in range(x_max * y_max):
    x_test = -1
    y_test = -1
    for y in range(y_max):
        for x in range(x_max):
            if not visited[y][x] and (
                    (x_test == -1 and y_test == -1) or number_of_steps[y][x] <= number_of_steps[y_test][x_test]):
                x_test = x
                y_test = y
    if number_of_steps[y_test][x_test] == np.Inf:
        break
    visited[y_test][x_test] = True
    for (x, y), stepsize in graph[(x_test, y_test)]:
        if number_of_steps[y_test][x_test] + stepsize <= number_of_steps[y][x]:
            number_of_steps[y][x] = number_of_steps[y_test][x_test] + stepsize

for y in range(y_max):
    print(" ".join(["{:3.0f}".format(step) for step in number_of_steps[y]]))
print(" ")
print(number_of_steps[y_end][x_end])
