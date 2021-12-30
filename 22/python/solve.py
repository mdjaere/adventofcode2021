import sys
from itertools import chain

verbose = False

infile = sys.argv[1] if len(sys.argv) > 1 else 'input'


instructions = [(
    line.strip()[0:3].strip(),
    tuple(int(c) for c in line[3:].strip().split(
        ",")[0].replace("x=", "").split("..")),
    tuple(int(c) for c in line[3:].strip().split(
        ",")[1].replace("y=", "").split("..")),
    tuple(int(c) for c in line[3:].strip().split(
        ",")[2].replace("z=", "").split(".."))
) for line in open(infile)]

coordinates = set()
for i_index, instruction in enumerate(instructions):
    cmd, x_range, y_range, z_range = instruction
    all_ranges = list(chain(x_range, y_range, z_range))
    if min(all_ranges) < -50 or max(all_ranges) > 50:
        continue
    for x in range(x_range[0], x_range[1]+1):
        for y in range(y_range[0], y_range[1]+1):
            for z in range(z_range[0], z_range[1]+1):
                p = x, y, z
                if cmd == "on":
                    coordinates.add(p)
                else:
                    if p in coordinates:
                        coordinates.remove(p)
    if verbose:
        print(f"After Instruction {i_index} {cmd}: {len(coordinates)}")

print("Part 1:", len(coordinates))


# Part 2

def create_new_ranges(existing_range, splitter_range):
    low, high = splitter_range

    def low_range_intersection():
        return existing_range[0] < low <= existing_range[1]

    def high_range_intersection():
        return existing_range[0] <= high < existing_range[1]

    def full_range_intersection():
        return low <= existing_range[0] < existing_range[1] <= high

    if low_range_intersection() and high_range_intersection():
        return [(existing_range[0], low - 1),
                (low, high),
                (high + 1, existing_range[1])], "both"
    elif low_range_intersection():
        return [(existing_range[0], low - 1), (low, existing_range[1])], "low"
    elif high_range_intersection():
        return [(existing_range[0], high), (high + 1, existing_range[1])], "high"
    elif full_range_intersection():
        return [existing_range], "full"
    else:  # No intersection
        return [existing_range], "none"


def split_block(block, split_block):
    finalised = []
    x_ranges, x_intersection_type = create_new_ranges(block[0], split_block[0])

    x_splitted = [(r, block[1], block[2]) for r in x_ranges]

    if x_intersection_type == "low":
        finalised.append(x_splitted[0])
        x_splitted = [x_splitted[1]]
    elif x_intersection_type == "high":
        finalised.append(x_splitted[1])
        x_splitted = [x_splitted[0]]
    elif x_intersection_type == "both":
        finalised.append(x_splitted[0])
        finalised.append(x_splitted[2])
        x_splitted = [x_splitted[1]]

    xy_splitted = []
    xy_intersections_types = []
    for x_block in x_splitted:
        y_ranges, y_intersection_type = create_new_ranges(
            x_block[1], split_block[1])
        xy_intersections_types.append(y_intersection_type)
        xy_splitted.append([(x_block[0], r, x_block[2]) for r in y_ranges])

    filtered_xy_splitted = []
    for index, y_intersection_type in enumerate(xy_intersections_types):
        if y_intersection_type == "low":
            finalised.append(xy_splitted[index][0])
            filtered_xy_splitted.append(xy_splitted[index][1])
        elif y_intersection_type == "high":
            finalised.append(xy_splitted[index][1])
            filtered_xy_splitted.append(xy_splitted[index][0])
        elif y_intersection_type == "both":
            finalised.append(xy_splitted[index][0])
            finalised.append(xy_splitted[index][2])
            filtered_xy_splitted.append(xy_splitted[index][1])
        else:
            filtered_xy_splitted.extend(xy_splitted[index])

    xyz_splitted = []
    for y_block in filtered_xy_splitted:
        z_ranges, z_intersection_type = create_new_ranges(
            y_block[2], split_block[2])
        xyz_splitted.extend([(y_block[0], y_block[1], r) for r in z_ranges])

    return finalised + xyz_splitted


def check_inclusion(block, ref_block):
    if not ref_block[0][0] <= (sum(block[0]) / 2) <= ref_block[0][1]:
        return False
    if not ref_block[1][0] <= (sum(block[1]) / 2) <= ref_block[1][1]:
        return False
    if not ref_block[2][0] <= (sum(block[2]) / 2) <= ref_block[2][1]:
        return False
    return True


def intersect(a, b):
    # From @gorset
    result = (
        (max(a[0][0], b[0][0]), min(a[0][1], b[0][1])),
        (max(a[1][0], b[1][0]), min(a[1][1], b[1][1])),
        (max(a[2][0], b[2][0]), min(a[2][1], b[2][1]))
    )
    if result[0][0] > result[0][1]:
        return None
    if result[1][0] > result[1][1]:
        return None
    if result[2][0] > result[2][1]:
        return None
    return result


def calc_volume(blocks):
    total = sum(
        (b[0][1] - b[0][0] + 1) *
        (b[1][1] - b[1][0] + 1) *
        (b[2][1] - b[2][0] + 1)
        for b in blocks)
    return total


to_keep = set()
for i, (cmd, x_range, y_range, z_range) in enumerate(instructions):
    if cmd == "on":
        temp_blocks = set([(x_range, y_range, z_range)])
        for f_index, (_, xr, yr, zr) in enumerate(instructions[i+1:]):
            op_block = xr, yr, zr
            to_delete = []
            to_add = []
            for existing_block in temp_blocks:
                intersection = intersect(op_block, existing_block)
                if not intersection:
                    continue
                splits = split_block(existing_block, intersection)
                filtered_temp_blocks = {sub_block for sub_block in splits if not check_inclusion(
                    sub_block, intersection)}
                to_add.extend(filtered_temp_blocks)
                to_delete.append(existing_block)
            temp_blocks.difference_update(to_delete)
            temp_blocks.update(to_add)
        to_keep.update(temp_blocks)
    if verbose:
        print(
            f"After Instruction {i} {cmd} - Volume: {calc_volume(to_keep)} Number of blocks: {len(to_keep)}")


volume = calc_volume(to_keep)

print("Part 2:", volume)
