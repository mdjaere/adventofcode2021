import sys
from itertools import chain

infile = sys.argv[1] if len(sys.argv) > 1 else 'input'

raw = open(infile).read()
raw_coordinates, raw_instructions = raw.split("\n\n")
dots = {tuple([int(x) for x in line.split(',')])
        for line in raw_coordinates.split("\n")}
instructions = [line.replace("fold along ", "").split(
    "=") for line in raw_instructions.split("\n")]

xs, ys = zip(*dots)

for index, cmd in enumerate(instructions):
    cmd_type, cmd_value = cmd
    cmd_value = int(cmd_value)
    new_dots = set()
    for dot in dots:
        if cmd_type == "y":
            new_order = tuple(chain(
                range(cmd_value),
                range(cmd_value, -1, -1)
            ))
            if dot[1] == cmd_value:
                continue
            else:
                d = dot[0], new_order[dot[1]]
                new_dots.add(d)
        if cmd_type == "x":
            new_order = tuple(chain(
                range(cmd_value * 2, cmd_value, -1),
                range(cmd_value, max(xs) + 1)
            ))
            if dot[0] == cmd_value:
                continue
            else:
                d = new_order[dot[0]] - (cmd_value + 1), dot[1]
                new_dots.add(d)
    dots = new_dots
    if index == 0:
        print("Part1:", len(dots))


print("Part 2:")

xs, ys = zip(*dots)
for x in range(min(xs), max(xs) + 1):
    row = []
    for y in range(min(ys), max(ys) + 1):
        if tuple([x, y]) in dots:
            row.append("#")
        else:
            row.append(" ")
    print("".join(row))
