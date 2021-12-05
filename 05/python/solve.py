import sys
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Pipe:
    start: Point
    end: Point
    vector = [0, 0]
    transform = [0, 0]

    def __post_init__(self):
        self.vector = [self.end.x - self.start.x, self.end.y - self.start.y]
        max_vec = max(abs(x) for x in self.vector)
        self.transform = [int(v / max_vec) for v in self.vector]


class Grid:
    def __init__(self, width, height):
        self.grid = [[0]*(width+1) for i in range(height+1)]

    def add_pipe(self, pipe, skip_diagonal=False):
        if skip_diagonal and not any(x == 0 for x in pipe.vector):
            return
        current = pipe.start
        while True:
            self.grid[current.y][current.x] += 1
            if current.x == pipe.end.x and current.y == pipe.end.y:
                break
            current = Point(
                current.x + pipe.transform[0], current.y + pipe.transform[1])

    def pipe_crossings(self):
        return sum(1 for row in self.grid for x in row if x >= 2)


def find_dimensions(pipes):
    width = [pipe.start.x for pipe in pipes] + [pipe.end.x for pipe in pipes]
    height = [pipe.start.y for pipe in pipes] + [pipe.end.y for pipe in pipes]
    return max(width), max(height)

infile = sys.argv[1] if len(sys.argv) > 1 else 'input'
lines = [pipe.strip("\n") for pipe in open(infile)]

pipes = [Pipe(*[Point(*[int(item) for item in pair.split(",")]) for pair in line.split(" -> ")])
         for line in lines]

dimensions = find_dimensions(pipes)

# Part 1

pipe_map_1 = Grid(*dimensions)

for pipe in pipes:
    pipe_map_1.add_pipe(pipe, skip_diagonal=True)

print(f"Part1: {pipe_map_1.pipe_crossings()}")

# Part 2

pipe_map_2 = Grid(*dimensions)

for pipe in pipes:
    pipe_map_2.add_pipe(pipe, skip_diagonal=False)

print(f"Part2: {pipe_map_2.pipe_crossings()}")
