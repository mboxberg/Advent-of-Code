from operator import itemgetter
import numpy as np


def touching(knot1, knot2):
    if abs(knot1[0] - knot2[0]) <= 1 and abs(knot1[1] - knot2[1]) <= 1:
        return True
    else:
        return False


def print_map(rope, start=(0, 0), print_on_screen=True, print_trace=False):
    map = ""
    min_col = min(min(rope, key=itemgetter(0))[0], start[0])
    max_col = max(max(rope, key=itemgetter(0))[0], start[0])
    min_row = min(min(rope, key=itemgetter(1))[1], start[1])
    max_row = max(max(rope, key=itemgetter(1))[1], start[1])
    for i_row in range(max_row, min_row - 1, -1):
        row = list("." * (max_col - min_col + 1))
        if i_row == start[1]:
            row[start[0] - min_col] = "s"
        for i_knot, knot in reversed(list(enumerate(rope))):
            if i_row == knot[1]:
                row[knot[0] - min_col] = "{}".format(i_knot) if not print_trace else "#"
        if i_row == rope[0][1] and not print_trace:
            row[rope[0][0] - min_col] = "H"
        if i_row == start[1] and print_trace:
            row[start[0] - min_col] = "s"
        map += "".join(row) + "\n"
    if print_on_screen:
        print(map)
    return map


directions = {"U": (1, 1),
              "D": (1, -1),
              "L": (0, -1),
              "R": (0, 1)}

print_all_maps = False
print_no_maps = False

n_knots = 10

rope = [(0, 0)] * n_knots
visited_positions = {rope[-1], rope[-1]}

with open("../dat/09") as input_file:
    while True:
        line = input_file.readline()
        if not line:
            break

        [direction, steps] = line.split()
        print("== {} {} ==\n".format(direction, steps))

        for i in range(int(steps)):
            head = list(rope[0])
            head[directions[direction][0]] += directions[direction][1]
            rope[0] = tuple(head)
            for j in range(1, n_knots):
                if not touching(rope[j], rope[j - 1]):
                    difference = (rope[j - 1][0] - rope[j][0], rope[j - 1][1] - rope[j][1])
                    tail = list(rope[j])
                    if np.abs(difference[0]) == np.abs(difference[1]):
                        tail[0] = tail[0] + np.sign(difference[0])
                        tail[1] = tail[1] + np.sign(difference[1])
                    else:
                        rope_direction = np.argmax(np.abs(difference))
                        tail[rope_direction] = tail[rope_direction] + np.sign(difference[rope_direction])
                        tail[(rope_direction + 1) % 2] = rope[j - 1][(rope_direction + 1) % 2]
                    rope[j] = tuple(tail)
            visited_positions.add(rope[-1])
            if print_all_maps and not print_no_maps:
                print_map(rope)
        if not print_all_maps and not print_no_maps:
            print_map(rope)

print("We visited {} positions at least once.".format(len(visited_positions)))
print_map(list(visited_positions), print_trace=True)
