import sys
import numpy as np
from copy import deepcopy


class Rock:
    def __init__(self, path):
        self.path = path

    @property
    def coordinates(self):
        positions = list()
        for i in range(len(self.path) - 1):
            dx = self.path[i + 1][0] - self.path[i][0]
            dy = self.path[i + 1][1] - self.path[i][1]
            if dx:
                for step in range(0, dx + np.sign(dx), np.sign(dx)):
                    positions.append((self.path[i][0] + step, self.path[i][1]))
            if dy:
                for step in range(0, dy + np.sign(dy), np.sign(dy)):
                    positions.append((self.path[i][0], self.path[i][1] + step))
        return positions


class Sand:
    def __init__(self, coordinate, moving=True):
        self.coordinate = coordinate
        self.moving = moving


class SandyCave:
    def __init__(self, rock_paths, sand_inflow, floor=False, floor_y=2):
        self.rock_paths = rock_paths
        self.sand_inflow = sand_inflow
        self.sands = list()
        self.not_air = list()
        self.floor = floor

        domain = list()
        for rock in self.rock_paths:
            domain.extend(rock.coordinates)
        domain.append(self.sand_inflow)
        min_x = min([coordinate[0] for coordinate in domain])
        max_x = max([coordinate[0] for coordinate in domain])
        min_y = min([coordinate[1] for coordinate in domain])
        max_y = max([coordinate[1] for coordinate in domain])
        if self.floor:
            max_y += floor_y
            min_x = min(min_x, self.sand_inflow[0] - (max_y - min_y))
            max_x = max(max_x, self.sand_inflow[0] + (max_y - min_y))
            self.rock_paths.append(Rock([(min_x, max_y), (max_x, max_y)]))
        self.domain = ((min_x, min_y), (max_x, max_y))
        for rock in self.rock_paths:
            self.not_air.extend(rock.coordinates)
        self.map_printed = False

    def insert_sand(self):
        if self.sand_inflow in self.not_air:
            raise RuntimeError("Sand inflow blocked.")
        else:
            self.sands.append(Sand(coordinate=self.sand_inflow))

    def material(self, coordinate):
        if coordinate == self.sand_inflow:
            return "+"
        for rock in self.rock_paths:
            if coordinate in rock.coordinates:
                return "#"
        for sand in self.sands:
            if coordinate == sand.coordinate:
                return "o"
        return "."

    def move_sand(self):
        number_of_moved_sand = 0
        for sand in self.sands:
            if sand.moving:
                for j in range(sand.coordinate[1], self.domain[1][1] + 1):
                    for i in [0, -1, 1]:
                        new_coordinate = (sand.coordinate[0] + i, sand.coordinate[1] + 1)
                        if not self.domain[0][0] <= new_coordinate[0] <= self.domain[1][0] or \
                                new_coordinate[1] > self.domain[1][1]:
                            raise RuntimeError('Cannot move sand: Sand would be outside of the domain.')
                        if new_coordinate not in self.not_air:
                            sand.coordinate = new_coordinate
                            break
                    else:
                        continue
                else:
                    sand.moving = False
                    number_of_moved_sand += 1
                    self.not_air.append(sand.coordinate)
                    break
        return number_of_moved_sand

    def print_map(self):
        column_digits = np.floor(np.log10(self.domain[1][0])) + 1 + int(self.domain[0][0] < 0)
        row_digits = np.floor(np.log10(self.domain[1][1])) + 1 + int(self.domain[0][1] < 0)

        for i in zip(*['{:>{n}f}'.format(i, n=column_digits) for i in range(self.domain[0][0], self.domain[1][0] + 1)]):
            print(" " * row_digits + "".join(i))
        for i in range(self.domain[0][1], self.domain[1][1] + 1):
            print("{row:{size}f}".format(row=i, size=row_digits) + "".join(
                [self.material((x, i)) for x in range(self.domain[0][0], self.domain[1][0] + 1)]))
        self.map_printed = True

    def erase_map(self):
        if self.map_printed:
            column_digits = int(np.floor(np.log10(self.domain[1][0])) + 1 + int(self.domain[0][0] < 0))
            for _ in range(self.domain[1][1] - self.domain[0][1] + column_digits):
                sys.stdout.write("\x1b[1A")  # cursor up one line
                sys.stdout.write("\x1b[2K")  # delete the line
            self.map_printed = False


if __name__ == "__main__":
    # This is a very inefficient solution to day 14.
    maximum_number_of_moves = -1

    data = open('../dat/14').read().strip()
    lines = [x for x in data.split('\n')]
    rocks = list()
    for line in lines:
        rocks.append(Rock([tuple([int(x) for x in coordinate.split(',')]) for coordinate in line.split(' -> ')]))
    cave = SandyCave(rocks, (500, 0), floor=True)
    # cave.print_map()

    number_of_sand_at_rest = 0
    i = 0
    while i < maximum_number_of_moves or maximum_number_of_moves < 0:
        i += 1
        try:
            cave.insert_sand()
            cave.move_sand()
            number_of_sand_at_rest += 1
            # cave.print_map()
            print(number_of_sand_at_rest)
        except RuntimeError:
            break
    # cave.print_map()
    print("{} units of sand came to rest.\n".format(number_of_sand_at_rest))
