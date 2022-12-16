class Valve:
    def __init__(self, name, flow_rate, tunnels, opened=False):
        self.name = name
        self.flow_rate = flow_rate
        self.tunnels = tunnels
        self.opened = opened

    def __str__(self):
        return ("Closed" if self.closed else "Opened") + " valve {} has flow rate={}; tunnels lead to valves ".format(
            self.name, self.flow_rate) + ", ".join(self.tunnels)

    @property
    def closed(self):
        return not self.opened

    @closed.setter
    def closed(self, is_closed):
        self.opened = not is_closed


if __name__ == "__main__":
    verbose = True

    data = open('../dat/16_example').read().strip()
    lines = [x for x in data.split('\n')]

    valves = dict()
    for line in lines:
        name = line.split(';')[0].split(" ")[1]
        flow_rate = int(line.split(';')[0].split(" ")[-1].split("=")[-1])
        tunnels = line.split(';')[1].split(', ')
        tunnels[0] = tunnels[0][-2:]
        valves[name] = Valve(name=name, flow_rate=flow_rate, tunnels=tunnels)

    if verbose:
        for valve in sorted(valves.values()):
            print(valve)
        print("")

    current_valve = valves["AA"]
    visited_valves = [current_valve.name]
    opened_valves = list()
    releasing_pressure = 0
    released_pressure = 0
    for t in range(1, 30 + 1):
        released_pressure += releasing_pressure
        if verbose:
            print("== Minute {} ==".format(t))
            if len(opened_valves) == 0:
                print("No valves are open.")
            elif len(opened_valves) == 1:
                print("Valve {} is open, releasing {} pressure.".format(opened_valves[0], releasing_pressure))
            else:
                print("Valves " + ", ".join(sorted(opened_valves)) + " are open, releasing {} pressure.".format(
                    releasing_pressure))

        tunnel_options = list()
        tunnel_flow_rates = list()
        max_flow_rate = 0
        for tunnel in current_valve.tunnels:
            if tunnel not in visited_valves and valves[tunnel].closed:
                tunnel_options.append(tunnel)
                tunnel_flow_rates.append(valves[tunnel].flow_rate)
        if len(tunnel_flow_rates) == 0:
            max_flow_rate == 0
        else:
            max_flow_rate = max(tunnel_flow_rates)

        if current_valve.opened:
            if tunnel_options:
                move_to = tunnel_options[0]
            else:
                move_to = current_valve.tunnels[-1]
        elif max_flow_rate > current_valve.flow_rate or current_valve.flow_rate == 0:
            if tunnel_options:
                move_to = tunnel_options[tunnel_flow_rates.index(max_flow_rate)]
            else:
                move_to = current_valve.tunnels[-1]
        else:
            move_to = ""
            current_valve.opened = True
            opened_valves.append(current_valve.name)
            releasing_pressure += current_valve.flow_rate
            if verbose:
                print("You open valve " + current_valve.name + ".")
        if move_to:
            current_valve = valves[move_to]
            visited_valves.append(current_valve.name)
            if verbose:
                print("You move to valve " + current_valve.name + ".")
        if verbose:
            print("")
    print("In total {} pressure were released in {} minutes.".format(released_pressure, t))
