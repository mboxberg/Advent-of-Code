"""
The jungle must be too overgrown and difficult to navigate in vehicles or access from the air; the Elves' expedition
traditionally goes on foot. As your boats approach land, the Elves begin taking inventory of their supplies. One
important consideration is food - in particular, the number of Calories each Elf is carrying (your puzzle input).

The Elves take turns writing down the number of Calories contained by the various meals, snacks, rations, etc. that
they've brought with them, one item per line. Each Elf separates their own inventory from the previous Elf's inventory
(if any) by a blank line.

For example, suppose the Elves finish writing their items' Calories and end up with the following list:

1000
2000
3000

4000

5000
6000

7000
8000
9000

10000

This list represents the Calories of the food carried by five Elves:

    The first Elf is carrying food with 1000, 2000, and 3000 Calories, a total of 6000 Calories.
    The second Elf is carrying one food item with 4000 Calories.
    The third Elf is carrying food with 5000 and 6000 Calories, a total of 11000 Calories.
    The fourth Elf is carrying food with 7000, 8000, and 9000 Calories, a total of 24000 Calories.
    The fifth Elf is carrying one food item with 10000 Calories.

In case the Elves get hungry and need extra snacks, they need to know which Elf to ask: they'd like to know how many
Calories are being carried by the Elf carrying the most Calories. In the example above, this is 24000 (carried by the
fourth Elf).

Find the Elf carrying the most Calories. How many total Calories is that Elf carrying?
"""

import numpy as np

# import file as string
with open("../dat/01") as input_file:
    input_str = input_file.read()

# split sting into values for the different elves (blank line seperates elves, new line seperates items of an elf)
elf_calories = [elf.split() for elf in input_str.split("\n\n")]
# convert everythin to integer
elf_calories = [map(int, calories) for calories in elf_calories]
# sum up calories for each elf and sort in ascending order
elf_calories = np.sort([sum(elf) for elf in elf_calories])
# find maximum calories
maximum_calories = max(elf_calories)

print("The Elf carrying the most Calories carries {} calories.".format(maximum_calories))

"""
By the time you calculate the answer to the Elves' question, they've already realized that the Elf carrying the most 
Calories of food might eventually run out of snacks.

To avoid this unacceptable situation, the Elves would instead like to know the total Calories carried by the top three 
Elves carrying the most Calories. That way, even if one of those Elves runs out of snacks, they still have two backups.

In the example above, the top three Elves are the fourth Elf (with 24000 Calories), then the third Elf (with 11000 
Calories), then the fifth Elf (with 10000 Calories). The sum of the Calories carried by these three elves is 45000.

Find the top three Elves carrying the most Calories. How many Calories are those Elves carrying in total?
"""

print("The top three Elves are carrying in totel {} calories.".format(sum(elf_calories[-3:])))
