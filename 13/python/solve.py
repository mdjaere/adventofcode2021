import sys
from itertools import chain
from collections import namedtuple

infile = sys.argv[1] if len(sys.argv) > 1 else 'input'

raw = open(infile).read()
raw_coordinates, raw_instructions = raw.split("\n\n")

Dot = namedtuple("Dot", ["x", "y"])

dots = {Dot(*[int(x) for x in line.split(',')])
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
            if dot.y == cmd_value:
                continue
            else:
                new_dots.add(Dot(dot.x, new_order[dot.y]))
        if cmd_type == "x":
            new_order = tuple(chain(
                range(cmd_value * 2, cmd_value, -1),
                range(cmd_value, max(xs) + 1)
            ))
            if dot.x == cmd_value:
                continue
            else:
                new_dots.add(
                    Dot(new_order[dot.x] - (cmd_value + 1), dot.y))
    dots = new_dots
    if index == 0:
        print("Part1:", len(dots))


print("Part 2:")

xs, ys = zip(*dots)
for x in range(min(xs), max(xs) + 1):
    row = []
    for y in range(min(ys), max(ys) + 1):
        if Dot(x, y) in dots:
            row.append("#")
        else:
            row.append(" ")
    print("".join(row))
