class Monkey:
    RELIEF_FACTOR = 3

    def __init__(self, number, starting_items, operation, test, throw_to_monkey):
        self.number = number
        self.items = starting_items
        self.operation = operation
        self.test = test
        self.throw_to_monkey = throw_to_monkey
        self.number_of_inspections = 0

    def do_operation(self, item, verbose):
        result = eval(self.operation, {"old": item})
        if verbose:
            print("    Worry level is changed to {}.".format(result))
        return result

    def do_test(self, item):
        return item % self.test == 0

    def relief(self, item, verbose=True):
        result = item // self.RELIEF_FACTOR
        if verbose:
            print("    Monkey gets bored with item. Worry level is divided by {} to {}.".format(self.RELIEF_FACTOR,
                                                                                                result))
        return result

    def round(self, other_monkeys, test_mod=1, relief=True, verbose=True):
        if verbose:
            print("Monkey {}:".format(self.number))
        for item in self.items:
            self.number_of_inspections += 1
            if verbose:
                print("  Monkey inspects an item with a worry level of {}.".format(item))
            item = self.do_operation(item, verbose)
            if relief:
                item = self.relief(item, verbose)
            item = item % test_mod
            if verbose:
                print("    Current worry level is {}divisible by {}".format("not " if not self.do_test(item) else "",
                                                                            self.test))
                print("    Item with worry level {} is thrown to monkey {}.".format(item, self.throw_to_monkey[
                    self.do_test(item)]))
            other_monkeys[self.throw_to_monkey[self.do_test(item)]].items.append(item)

        self.items = []

    def print_items(self):
        print("Monkey {}: ".format(self.number) + ", ".join(map(str, self.items)))


if __name__ == "__main__":
    monkeys = []
    number_of_rounds = 10000  # 20
    relief = False
    verbose = False
    test_mod = 1
    save_time = True

    # read input
    with open("../dat/11") as input_file:
        while True:
            line = input_file.readline()
            if not line:
                break
            if line.startswith("Monkey"):
                throw_to = dict()
                number = int(line[:-2].split(" ")[1])
                items = [int(item) for item in input_file.readline()[:-1].split(":")[1].split(",")]
                operation = "".join(input_file.readline()[:-1].split(" ")[-3:])
                test = int(input_file.readline()[:-1].split(" ")[-1])
                if save_time:
                    test_mod *= test
                throw_to[True] = int(input_file.readline()[:-1].split(" ")[-1])
                throw_to[False] = int(input_file.readline()[:-1].split(" ")[-1])
                monkeys.append(Monkey(number, items, operation, test, throw_to))

    for i in range(number_of_rounds):
        for monkey in monkeys:
            monkey.round(monkeys, test_mod=test_mod, relief=relief, verbose=verbose)
        if verbose:
            print("\nAfter round {}, the monkeys are holding items with these worry levels:".format(i + 1))
            for monkey in monkeys:
                monkey.print_items()
            print("")

    for monkey in monkeys:
        print("Monkey {} inspected items {} times.".format(monkey.number, monkey.number_of_inspections))
    print("")
    monkey_business_list = sorted([monkey.number_of_inspections for monkey in monkeys], reverse=True)
    monkey_business_level = monkey_business_list[0] * monkey_business_list[1]
    print("Monkey business level is {}.".format(monkey_business_level))
