import sys
from collections import namedtuple
from copy import deepcopy

infile = sys.argv[1] if len(sys.argv) > 1 else 'input'
grid_0 = [[int(c) for c in row.strip()] for row in open(infile)]

Point = namedtuple("Point", ["x", "y"])


def get_block(mid_p, grid):
    x, y = mid_p
    block = set()
    for nx in [x + dx for dx in range(-1, 2) if 0 <= x + dx < len(grid[0])]:
        for ny in [y + dy for dy in range(-1, 2) if 0 <= y + dy < len(grid[0])]:
            block.add(Point(nx, ny))
    return block


def iterate(grid):
    flash_count = 0
    flashing = []
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            grid[y][x] += 1
            if grid[y][x] == 10:
                flashing.append(Point(x, y))
                flash_count += 1
    while flashing:
        point = flashing.pop()
        for p in get_block(point, grid):
            grid[p.y][p.x] += 1
            if grid[p.y][p.x] == 10:
                flashing.append(p)
                flash_count += 1
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] > 9:
                grid[y][x] = 0

    return grid, flash_count

# Part 1


grid = deepcopy(grid_0)

total_flashes = 0
for step in range(100):
    grid, flash_count = iterate(grid)
    total_flashes += flash_count
print(f"Part 1: {total_flashes}")


# Part 2

grid = deepcopy(grid_0)

step = 0
while True:
    grid, flash_count = iterate(grid)
    step += 1
    if flash_count == len(grid) * len(grid[0]):
        break

print(f"Part2: {step}")
