import numpy as np

i = 0
j = 0
double_items = list()

group_rucksacks = ["", "", ""]
group_badges = list()


def priority(item):
    return ord(item) - 96 if ord(item) >= 97 else ord(item) - 64 + 26


with open("../dat/03") as input_file:
    while True:
        i += 1
        rucksack = input_file.readline()
        if not rucksack:
            break
        else:
            group_rucksacks[i % 3] = rucksack[:-1]

        compartment1 = rucksack[:len(rucksack) // 2]
        compartment2 = rucksack[len(rucksack) // 2:-1]

        for item in compartment1:
            if item in compartment2:
                double_items.append(item)
                break

        if i % 3 == 0:
            for item in group_rucksacks[0]:
                if item in group_rucksacks[1] and item in group_rucksacks[2]:
                    group_badges.append(item)
                    break

print(len(double_items))
priorities = [priority(item) for item in double_items]
print(zip(double_items, priorities))
priority_sum = np.array(priorities).sum()
print(priority_sum)

print("")

print(len(group_badges))
group_priorities = [priority(item) for item in group_badges]
print(zip(group_badges, group_priorities))
group_priority_sum = np.array(group_priorities).sum()
print(group_priority_sum)
