import sys

infile = sys.argv[1] if len(sys.argv) > 1 else 'input'

input = open(infile).readline().strip().replace("target area: ", "").split(",")
x_target = [int(x) for x in input[0].replace("x=", "").split("..")]
y_target = [int(y) for y in input[1].replace("y=", "").split("..")]


class Probe():
    def __init__(self, x_vel, y_vel):
        self.x = 0
        self.y = 0
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.trajectory = [(self.x, self.y)]

    def step(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.trajectory.append((self.x, self.y))
        self.x_vel = self.x_vel - 1 if self.x_vel > 0 else 0
        self.y_vel = self.y_vel - 1


trajectories = []
max_y = 0
valid_settings = []

for x_vel in range(1, 200, 1):
    for y_vel in range(-200, 300, 1):
        probe = Probe(x_vel, y_vel)
        while probe.x < x_target[1] and probe.y > y_target[0]:
            probe.step()
        # trajectories.append(probe.trajectory)
        if any(x_target[0] <= x <= x_target[1] and y_target[0] <= y <= y_target[1] for x, y in probe.trajectory):
            top = max(y for x, y in probe.trajectory)
            if top > max_y:
                max_y = top
                # print(max_y, (x_vel, y_vel))
            # trajectories.append(probe.trajectory)
            valid_settings.append((x_vel, y_vel))

print(f"Part1: {max_y}")
print(f"Part2: {len(valid_settings)}")

# Will draw trajectories
if False:
    for y in range(100, y_target[0], -1):
        row = ""
        for x in range(-3, x_target[1]):
            coor = x, y

            if x == 0 and y == 0:
                row += " S"
            elif any(coor in traj for traj in trajectories):
                row += " @"
            if x_target[0] <= x <= x_target[1] and y_target[0] <= y <= y_target[1]:
                row += " _"
            else:
                row += " ."
        print(row)
