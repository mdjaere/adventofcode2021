# dag 9


import sys
from functools import reduce

infile = sys.argv[1] if len(sys.argv) > 1 else 'input'
floor_map = [[int(c) for c in line.strip()] for line in open(infile)]

low_coords = set()

for y, row in enumerate(floor_map):
    for x, v in enumerate(row):
        compare_to = []
        if y != 0:
            compare_to.append(floor_map[y-1][x])
        if y != len(floor_map) - 1:
            compare_to.append(floor_map[y+1][x])
        if x != 0:
            compare_to.append(floor_map[y][x-1])
        if x != len(row) - 1:
            compare_to.append(floor_map[y][x+1])
        checks = [v < c for c in compare_to]
        if all(checks):
            low_coords.add(tuple([x, y]))

r = sum([floor_map[y][x] for x, y in iter(low_coords)]) + len(low_coords)
print("Part 1:", r)


def basin_count(point, seen=set()):
    x, y = point
    if point in seen:
        return 0
    seen.add(point)
    if floor_map[y][x] == 9:
        return 0
    count = 0
    if y != 0:
        count += basin_count(tuple([x, y-1]), seen)
    if y != len(floor_map) - 1:
        count += basin_count(tuple([x, y+1]), seen)
    if x != 0:
        count += basin_count(tuple([x-1, y]), seen)
    if x != len(floor_map[0]) - 1:
        count += basin_count(tuple([x+1, y]), seen)
    return 1 + count

# Using low point basins only


basins_low_points = []
for point in low_coords:
    basins_low_points.append(basin_count(point))

r1 = reduce(lambda a, x: a*x, sorted(basins_low_points, reverse=True)[0:3])
print(f"Part 2 - Low point bains only: {r1}")

# Checking all points

seen = set()
basins = []
for y, row in enumerate(floor_map):
    for x, v in enumerate(row):
        point = x, y
        if point not in seen:
            basins.append(basin_count(point, seen))

r2 = reduce(lambda a, x: a*x, sorted(basins, reverse=True)[0:3])
print(f"Part 2 - Checking all points : {r2}")
