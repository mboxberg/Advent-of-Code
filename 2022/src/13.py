def parse(string):
    if len(string) == 0:
        return list()
    try:
        return int(string)
    except ValueError:
        opened_bracket = 0
        closed_bracket = 0
        items = []
        item = ''
        for character in string:
            if character == '[':
                opened_bracket += 1
                if opened_bracket - closed_bracket > 1:
                    item += character
            elif character == ']':
                closed_bracket += 1
                if opened_bracket - closed_bracket > 0:
                    item += character
                elif opened_bracket == closed_bracket:
                    if len(item) > 0:
                        items.append(parse(item))
                    item = ''
            elif character == ',':
                if opened_bracket == closed_bracket + 1:
                    if len(item) > 0:
                        items.append(parse(item))
                    item = ''
                else:
                    item += character
            else:
                item += character
        return items


def right_order(left, right, level=0, verbose=False):
    if verbose:
        print('  ' * level + '- Compare {} vs {}'.format(left, right))
    if type(left) == int and type(right) == int:
        if left < right:
            if verbose:
                print('  ' * level + '  - Left side is smaller, so inputs are in the right order')
            return True
        elif left == right:
            return None
        else:
            if verbose:
                print('  ' * level + '  - Right side is smaller, so inputs are not in the right order')
            return False
    if type(right) == int:
        if verbose:
            print('  ' * level + '  - Mixed types; convert right to [{}] and retry comparison'.format(right))
        return right_order(left, [right], level=level + 1, verbose=verbose)
    if type(left) == int:
        if verbose:
            print('  ' * level + '  - Mixed types; convert left to [{}] and retry comparison'.format(left))
        return right_order([left], right, level=level + 1, verbose=verbose)

    if len(left) == 0:
        if len(right) == 0:
            return None
        if verbose:
            print('  ' * level + '  - Left side ran out of items, so inputs are in the right order')
        return True
    if len(right) == 0:
        if len(left) == 0:
            return None
        if verbose:
            print('  ' * level + '  - Right side ran out of items, so inputs are not in the right order')
        return False

    if len(left) < len(right):
        left.append([])
    else:
        right.append([])

    n_items = max(len(left), len(right))
    for left_item, right_item in zip(left[:n_items], right[:n_items]):
        items_are_in_right_order = right_order(left_item, right_item, level=level + 1, verbose=verbose)
        if items_are_in_right_order is not None:
            return items_are_in_right_order
    if len(left) == n_items:
        return

    return None


verbose = True
data = open('../dat/13').read().strip()
line_pairs = [[y for y in x.split('\n')] for x in data.split('\n\n')]

packets = dict()
for i, pair in enumerate(line_pairs):
    packet = {"left": parse(pair[0]), "right": parse(pair[1])}
    packets[i + 1] = packet

right_order_sum = 0
for i, pair in packets.items():
    if verbose:
        print('== Pair {} =='.format(i))
    pair_is_in_right_order = right_order(pair['left'], pair['right'], verbose=verbose)
    right_order_sum += i if pair_is_in_right_order else 0
    print("")

print("The sum of the indices of the pairs in the right order is {}".format(right_order_sum))

signal = list()
for pair in packets.values():
    signal.append(pair['left'])
    signal.append(pair['right'])
# Include divider packets
divider_packets = [[[2]], [[6]]]
for divider_packet in divider_packets:
    signal.append(divider_packet)

n = len(signal)
swapped = False
for i in range(n - 1):
    for j in range(n - i - 1):
        if not right_order(signal[j], signal[j + 1]):
            swapped = True
            signal[j], signal[j + 1] = signal[j + 1], signal[j]
    if not swapped:
        break

decoder_key = 1
for divider_packet in divider_packets:
    decoder_key *= signal.index(divider_packet) + 1
print("The decoder key for the distress signal is {}.".format(decoder_key))
