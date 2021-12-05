import sys
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Vent:
    start: Point
    end: Point
    vector = [0, 0]
    transform = [0, 0]

    def __post_init__(self):
        self.vector = [self.end.x - self.start.x, self.end.y - self.start.y]
        max_vec = max(abs(x) for x in self.vector)
        self.transform = [int(v / max_vec) for v in self.vector]


class VentMap:
    def __init__(self, width, height):
        self.map = [[0]*(width+1) for i in range(height+1)]

    def add_vent(self, vent, skip_diagonal=False):
        if skip_diagonal and not any(x == 0 for x in vent.vector):
            return
        current = vent.start
        while True:
            self.map[current.y][current.x] += 1
            if current.x == vent.end.x and current.y == vent.end.y:
                break
            current = Point(
                current.x + vent.transform[0], current.y + vent.transform[1])

    def vent_crossings(self):
        return sum(1 for row in self.map for x in row if x >= 2)


def find_dimensions(vents):
    width = [vent.start.x for vent in vents] + [vent.end.x for vent in vents]
    height = [vent.start.y for vent in vents] + [vent.end.y for vent in vents]
    return max(width), max(height)

# Start


infile = sys.argv[1] if len(sys.argv) > 1 else 'input'
lines = [vent.strip("\n") for vent in open(infile)]

vents = [Vent(*[Point(*[int(item) for item in pair.split(",")]) for pair in line.split(" -> ")])
         for line in lines]

dimensions = find_dimensions(vents)

# Part 1

vent_map_1 = VentMap(*dimensions)

for vent in vents:
    vent_map_1.add_vent(vent, skip_diagonal=True)

print(f"Part1: {vent_map_1.vent_crossings()}")

# Part 2

vent_map_2 = VentMap(*dimensions)

for vent in vents:
    vent_map_2.add_vent(vent, skip_diagonal=False)

print(f"Part2: {vent_map_2.vent_crossings()}")
