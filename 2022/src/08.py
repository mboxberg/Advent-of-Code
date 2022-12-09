import numpy as np


def get_scenic_score(height, trees, reverse=False):
    step = -1 if reverse else 1
    score = 0
    for tree in trees[::step]:
        score += 1
        if tree >= height:
            break
    return score


tree_map = list()

with open("../dat/08") as input_file:
    while True:
        line = input_file.readline()
        if not line:
            break
        tree_map.append([int(tree) for tree in line[:-1]])

tree_map = np.array(tree_map)

n_rows, n_columns = tree_map.shape
print(n_rows, n_columns)
print("")
print(tree_map)
print("")

tree_visible = np.zeros(tree_map.shape, dtype=int)
scenic_score = np.zeros(tree_map.shape, dtype=int)

for (row, column), tree_height in np.ndenumerate(tree_map):
    trees_left = tree_map[row, :column]
    trees_right = tree_map[row, column + 1:]
    trees_above = tree_map[:row, column]
    trees_below = tree_map[row + 1:, column]

    # check if tree is visible from outside
    if row == 0 or column == 0 or row == n_rows - 1 or column == n_columns - 1 or \
            all(tree_height > trees_left) or all(tree_height > trees_right) or \
            all(tree_height > trees_above) or all(tree_height > trees_below):
        tree_visible[row, column] = 1

    # count the trees visible from a given tree
    scenic_score[row, column] = get_scenic_score(tree_height, trees_left, True) * \
                                get_scenic_score(tree_height, trees_right, False) * \
                                get_scenic_score(tree_height, trees_above, True) * \
                                get_scenic_score(tree_height, trees_below, False)

print(tree_visible)
print(np.sum(tree_visible))
print("")

print(scenic_score)
print(np.max(scenic_score))
