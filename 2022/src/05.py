import numpy as np

new_mover = True  # True = CrateMover 9001, False = CrateMover 9000

crates = True
stacks = list()
moves = list()
supplies = dict()

with open("../dat/05") as input_file:
    while True:
        line = input_file.readline()
        if not line:
            break

        if line.startswith(" 1 "):
            crates = False
            supplies = {int(stack): list() for stack in line.split()}
            continue

        if crates:
            n = (len(line) + 1) // 4
            stacks.append([line[i * 4 + 1] for i in range(n)])
        elif line.startswith("move"):
            moves.append(line[:-1])

stacks = np.array(list(reversed(stacks)))
for i in range(n):
    for stack in stacks[:, i]:
        if stack.split():
            supplies[i + 1].append(stack)

print(supplies)

for move in moves:
    print(move)
    task = move.split()
    number = int(task[1])
    origin = int(task[3])
    target = int(task[5])

    if new_mover:
        supplies[target].extend(supplies[origin][-number:])
        del supplies[origin][-number:]
    else:
        for i in range(number):
            supplies[target].extend(supplies[origin][-1])
            supplies[origin].pop(-1)

    print(supplies)

print("".join([supplies[i + 1][-1] for i in range(n)]))
