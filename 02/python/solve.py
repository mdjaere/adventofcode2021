import fileinput
from dataclasses import dataclass


@dataclass
class Sub_cmd:
    direction: str
    value: int

    def __post_init__(self):
        self.value = int(self.value)


@dataclass
class Submarine:
    hor_pos: int = 0
    depth: int = 0
    aim: int = 0

    def navigate(self, cmd: Sub_cmd):
        if cmd.direction == "down":
            self.depth += cmd.value
        if cmd.direction == "up":
            self.depth -= cmd.value
        if cmd.direction == "forward":
            self.hor_pos += cmd.value

    def navigate_with_aim(self, cmd: Sub_cmd):
        if cmd.direction == "down":
            self.aim += cmd.value
        if cmd.direction == "up":
            self.aim -= cmd.value
        if cmd.direction == "forward":
            self.hor_pos += cmd.value
            self.depth += self.aim * cmd.value

    def result(self):
        return self.hor_pos * self.depth


lines = [line.strip() for line in fileinput.input()]
data = [Sub_cmd(*line.split()) for line in lines]
sub = Submarine()

for cmd in data:
    sub.navigate(cmd)

print(f"Part1: {sub.result()}")

####

sub2 = Submarine()
for cmd in data:
    sub2.navigate_with_aim(cmd)

print(f"Part2: {sub2.result()}")
