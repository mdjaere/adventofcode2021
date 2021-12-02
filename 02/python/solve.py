import fileinput
lines = [line.strip() for line in fileinput.input()]
data = [ line.split() for line in lines]

hor_pos = 0  # horizontal position
depth = 0  # depth

for cmd in data:
    direction, value = cmd
    if direction == "down":
        depth += int(value)
    if direction == "up":
        depth -= int(value)
    if direction == "forward":
        hor_pos += int(value)

result = hor_pos * depth
print( f"Part1: {result}")

hor_pos = 0  # horizontal position
depth = 0  # depth
aim = 0  # aim

for cmd in data:
    print(cmd)
    direction, value = cmd
    if direction == "down":
        aim += int(value)
    if direction == "up":
        aim -= int(value)
    if direction == "forward":
        hor_pos += int(value)
        depth += aim * int(value)
    print(hor_pos, depth, aim)

result = hor_pos * depth
print( f"Part2: {result}")