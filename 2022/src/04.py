fully_contained = 0
double_assigments = 0

with open("../dat/04") as input_file:
    while True:
        line = input_file.readline()
        if not line:
            break

        pair = line[:-1].split(",")
        elf1 = pair[0].split("-")
        elf2 = pair[1].split("-")

        if int(elf2[0]) <= int(elf1[0]) <= int(elf2[1]) or int(elf2[0]) <= int(elf1[1]) <= int(elf2[1]) or \
                int(elf1[0]) <= int(elf2[0]) <= int(elf1[1]) or int(elf1[0]) <= int(elf2[1]) <= int(elf1[1]):
            double_assigments += 1

        if int(elf2[0]) <= int(elf1[0]) <= int(elf2[1]) and int(elf2[0]) <= int(elf1[1]) <= int(elf2[1]) or \
                int(elf1[0]) <= int(elf2[0]) <= int(elf1[1]) and int(elf1[0]) <= int(elf2[1]) <= int(elf1[1]):
            fully_contained += 1

        print(line[:-1], elf1, elf2, double_assigments, fully_contained)

print(double_assigments)
print(fully_contained)
