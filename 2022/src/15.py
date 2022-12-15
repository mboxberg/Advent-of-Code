import numpy as np


def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


class Sensor:
    def __init__(self, pos, pos_closest_beacon):
        self.pos = pos
        self.closest_beacon = pos_closest_beacon

    def __str__(self):
        return "Sensor at x={}, y={}: closest beacon is at x={}, y={}".format(self.pos[0], self.pos[1],
                                                                              self.closest_beacon[0],
                                                                              self.closest_beacon[1])

    @property
    def distance(self):
        return manhattan_distance(self.pos, self.closest_beacon)

    def covered_by_sensor(self, other_pos):
        """Return whether the given position is covered by the sensor."""
        return self.distance >= manhattan_distance(self.pos, other_pos)


if __name__ == "__main__":
    verbose = True
    find_possible_beacon_only = True

    data = open('../dat/15').read().strip()
    lines = [x for x in data.split('\n')]

    sensors = list()
    for line in lines:
        sensor_info, beacon_info = tuple(line.split(":"))
        pos_sensor = [int(part.split("=")[-1]) for part in sensor_info.split(",")]
        pos_beacon = [int(part.split("=")[-1]) for part in beacon_info.split(",")]
        sensors.append(Sensor(pos_sensor, pos_beacon))

    x_min = np.Inf
    x_max = -np.Inf
    y_min = np.inf
    y_max = -np.Inf

    for sensor in sensors:
        x_min = min([x_min, sensor.pos[0] - sensor.distance])
        x_max = max([x_max, sensor.pos[0] + sensor.distance])
        y_min = min([y_min, sensor.pos[1] - sensor.distance])
        y_max = max([y_max, sensor.pos[1] + sensor.distance])

        if verbose:
            print(sensor)
    if verbose:
        print("")

    n_covered = 0
    area_x = [0, 4000000]  # [0, 4000000]  # [0, 20]  # [x_min, x_max]
    area_y = [0, 4000000]  # [0, 4000000]  # [0, 20]  # [2000000, 2000000]  # [10, 10]
    sensors_to_consider = []
    possible_beacon_pos = list()
    for sensor in sensors:
        if sensor.pos[1] - sensor.distance <= area_y[1] and area_y[0] <= sensor.pos[1] + sensor.distance and \
                sensor.pos[0] - sensor.distance <= area_x[1] and area_x[0] <= sensor.pos[0] + sensor.distance:
            sensors_to_consider.append(sensor)
            if find_possible_beacon_only:
                for dx in range(sensor.distance + 1 + 1):
                    dy = (sensor.distance + 1) - dx
                    for x, y in [(sensor.pos[0] + dx, sensor.pos[1] + dy),
                                 (sensor.pos[0] + dx, sensor.pos[1] - dy),
                                 (sensor.pos[0] - dx, sensor.pos[1] + dy),
                                 (sensor.pos[0] - dx, sensor.pos[1] - dy)]:
                        if area_x[0] <= x <= area_x[1] and area_y[0] <= y <= area_y[1]:
                            for other_sensor in sensors:
                                if other_sensor.covered_by_sensor([x, y]):
                                    break
                            else:
                                possible_beacon_pos.append([x, y])
                                break
                    else:
                        continue
                    break
                else:
                    continue
                break

    length_label = max([len(str(area_y[0])), len(str(area_y[1]))])
    if not find_possible_beacon_only:
        if verbose:
            print(" " * (length_label + 1) + "| <- ({})".format(x_min))
        for y in range(area_y[0], area_y[1] + 1):
            covered = ""
            for x in range(area_x[0], area_x[1] + 1):
                for sensor in sensors_to_consider:
                    if sensor.covered_by_sensor([x, y]):
                        if manhattan_distance(sensor.closest_beacon, [x, y]) == 0:
                            covered += "B"
                        elif manhattan_distance(sensor.pos, [x, y]) == 0:
                            covered += "S"
                        else:
                            covered += "#"
                            n_covered += 1
                        break
                else:
                    covered += "."
                    possible_beacon_pos.append([x, y])
                    if find_possible_beacon_only:
                        break
            else:
                if verbose:
                    print("{0:{2}d} {1}".format(y, covered, length_label))
                if find_possible_beacon_only:
                    continue
            if verbose:
                print("{0:{2}d} {1}".format(y, covered, length_label))
            if find_possible_beacon_only:
                break
        if verbose:
            print("")
        if not find_possible_beacon_only:
            print("In the area where x={}, y={}, there are {} positions where a beacon cannot be present".format(area_x,
                                                                                                                 area_y,
                                                                                                                 n_covered))

    print("There is {} possible beacon location left.".format(len(possible_beacon_pos)))
    for beacon in possible_beacon_pos:
        print(" - {} (tuning frequency = {})".format(beacon, beacon[0] * 4000000 + beacon[1]))
