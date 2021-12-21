import sys
from typing import NamedTuple

infile = sys.argv[1] if len(sys.argv) > 1 else 'input'

sensors = []


class Point(NamedTuple):
    x: int = 0
    y: int = 0
    z: int = 0


class Sensor():
    def __init__(self):
        self.items = list()
        self.x_index = -1
        self.x_flipped = False
        self.x_offset = 0
        self.y_index = -1
        self.y_flipped = False
        self.y_offset = 0
        self.z_index = -1
        self.z_flipped = False
        self.z_offset = 0
        self.locked = False

    def get_xs(self):
        if self.x_flipped:
            values = [-c[self.x_index] for c in self.items]
        else:
            values = [c[self.x_index] for c in self.items]
        return [v + self.x_offset for v in values]

    def get_ys(self):
        if self.y_flipped:
            values = [-c[self.y_index] for c in self.items]
        else:
            values = [c[self.y_index] for c in self.items]
        return [v + self.y_offset for v in values]

    def get_zs(self):
        if self.z_flipped:
            values = [-c[self.z_index] for c in self.items]
        else:
            values = [c[self.z_index] for c in self.items]
        return [v + self.z_offset for v in values]

    def get_items_by_axis(self):
        return list(zip(*self.items))

    def get_beacons(self):
        return list(zip(self.get_xs(), self.get_ys(), self.get_zs()))

    def get_position(self):
        return Point(self.x_offset, self.y_offset, self.z_offset)


id = -1
for line in open(infile):
    if line.startswith("---"):
        id += 1
        sensors.append(Sensor())
    elif line.strip():
        data = Point(*[int(x) for x in line.strip().split(",")])
        sensors[id].items.append(data)

sensors[0].x_index = 0
sensors[0].y_index = 1
sensors[0].z_index = 2
sensors[0].locked = True
locked = [id for id, sensor in enumerate(sensors) if sensor.locked]
print("#" * len(locked) + "-"*(len(sensors) - len(locked)), end="\r")
while len(locked) < len(sensors):
    for sensor_id, cand_sensor in enumerate(sensors):
        if sensor_id in locked:
            continue
        for ref_id in locked:
            ref_sensor = sensors[ref_id]

            xs, ys, zs = cand_sensor.get_items_by_axis()
            alternatives = [xs,  # index 0
                            ys,  # index 1
                            zs,  # index 2
                            [-x for x in xs],  # index 0 reversed
                            [-x for x in ys],  # index 1 reversed
                            [-x for x in zs]  # index 2 reversed
                            ]
            # Solve X
            x_solved = False
            for alt_id, alt_axis in enumerate(alternatives):
                for ref_x in ref_sensor.get_xs():
                    for cand_x in alt_axis:
                        candidate_offset = ref_x - cand_x
                        offsets = [x + candidate_offset for x in alt_axis]
                        for v in ref_sensor.get_xs():
                            if v in offsets:
                                offsets.remove(v)
                        if len(alt_axis) - len(offsets) > 11:
                            sensors[sensor_id].x_offset = candidate_offset
                            if alt_id in [0, 1, 2]:
                                alternatives[alt_id] = []
                                alternatives[alt_id + 3] = []
                                sensors[sensor_id].x_index = alt_id
                            else:
                                alternatives[alt_id - 3] = []
                                alternatives[alt_id] = []
                                sensors[sensor_id].x_flipped = True
                                sensors[sensor_id].x_index = alt_id - 3
                            x_solved = True
                        if x_solved:
                            break
                    if x_solved:
                        break
                if x_solved:
                    break
            # Solve Y
            y_solved = False
            for alt_id, alt_axis in enumerate(alternatives):
                if not alt_axis:
                    continue
                for ref_y in ref_sensor.get_ys():
                    for cand_y in alt_axis:
                        candidate_offset = ref_y - cand_y
                        offsets = [x + candidate_offset for x in alt_axis]
                        for v in ref_sensor.get_ys():
                            if v in offsets:
                                offsets.remove(v)
                        if len(alt_axis) - len(offsets) > 11:
                            sensors[sensor_id].y_offset = candidate_offset
                            if alt_id in [0, 1, 2]:
                                alternatives[alt_id] = []
                                alternatives[alt_id + 3] = []
                                sensors[sensor_id].y_index = alt_id
                            else:
                                alternatives[alt_id - 3] = []
                                alternatives[alt_id] = []
                                sensors[sensor_id].y_flipped = True
                                sensors[sensor_id].y_index = alt_id - 3
                            y_solved = True
                        if y_solved:
                            break
                    if y_solved:
                        break
                if y_solved:
                    break
            # Solve Z
            z_solved = False
            for alt_id, alt_axis in enumerate(alternatives):
                if not alt_axis:
                    continue
                for ref_z in ref_sensor.get_zs():
                    for cand_z in alt_axis:
                        candidate_offset = ref_z - cand_z

                        offsets = [x + candidate_offset for x in alt_axis]
                        for v in ref_sensor.get_zs():
                            if v in offsets:
                                offsets.remove(v)

                        if len(alt_axis) - len(offsets) > 11:
                            sensors[sensor_id].z_offset = candidate_offset
                            if alt_id in [0, 1, 2]:
                                sensors[sensor_id].z_index = alt_id
                            else:
                                sensors[sensor_id].z_flipped = True
                                sensors[sensor_id].z_index = alt_id - 3
                            z_solved = True
                        if z_solved:
                            break
                    if z_solved:
                        break
                if z_solved:
                    break
            # Hopefully they should all be solved
            if all([x_solved, y_solved, z_solved]):
                cand_sensor.locked = True
                break
            # else:
            #     print("Not solved - trying another locked sensor")
        if cand_sensor.locked:
            break
    locked = [id for id, sensor in enumerate(sensors) if sensor.locked]
    print("#" * len(locked) + "-"*(len(sensors) - len(locked)), end="\r")
print()

all_beacons = {beacon for sensor in sensors for beacon in sensor.get_beacons()}

print("Part 1:", len(all_beacons))

all_sensor_positions = [sensor.get_position() for sensor in sensors]
max_manhattan = 0
for a in all_sensor_positions:
    for b in all_sensor_positions:
        max_manhattan = max(
            max_manhattan,
            abs(b.x - a.x) + abs(b.y - a.y) + abs(b.z - a.z)
        )


print("Part 2:", max_manhattan)
