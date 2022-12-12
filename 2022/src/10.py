cycle = 0
register = 1
busy = False
signal_strength = 0
sum_of_interesting_signal_strengths = 0

crt_width = 40
crt_height = 6
crt = ""

sprite_width = 3

with open("../dat/10") as input_file:
    while True:
        cycle += 1
        signal_strength = cycle * register

        if (cycle + 20) % 40 == 0:
            sum_of_interesting_signal_strengths += signal_strength

        crt += "#" if abs(register - ((cycle - 1) % crt_width)) <= (sprite_width - 1) // 2 else "."
        if cycle % crt_width == 0:
            crt += "\n"

        if not busy:
            line = input_file.readline()
            if not line:
                break

            # get command from line
            if line[-1] == "\n":
                command = line[:-1].split(" ")
            else:
                command = line.split(" ")

            if command[0] == "noop":
                cycle
            elif command[0] == "addx":
                busy = True
                register_addx = int(command[1])
        else:
            register += register_addx
            busy = False

        print("{:4d} ({}): {:4d}   (signal strength = {:6d})".format(cycle, "busy" if busy else "free", register,
                                                                     signal_strength))

print("The sum of the interesting signal strengths is {}".format(sum_of_interesting_signal_strengths))

print()
print(crt)
