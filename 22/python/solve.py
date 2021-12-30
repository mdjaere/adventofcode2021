import sys
from itertools import chain
from collections import deque


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

print("PART 1")
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
    print(f"After Instruction {i_index} {cmd}: {len(coordinates)}")

print("Part1", len(coordinates))


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
    _, y_intersection_type = create_new_ranges(block[1], split_block[1])
    _, z_intersection_type = create_new_ranges(block[2], split_block[2])
    if all(item == "none" for item in [x_intersection_type, y_intersection_type, z_intersection_type]):
        return [block]

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


# This block-reducer works well up to a few thousand blocks, but after instruction 386 I have 23,155,800+ blocks, which makes the reducer unusable.
# Disabled


def simplify_blocks(blocks=None):
    if blocks == None:
        blocks = set()
    # Not used
    in_length = len(blocks)
    print(f"Simplfying {in_length} ...", end="\r")
    stack = deque(blocks)
    while stack:
        block = stack.popleft()
        if len(stack) % 100 == 0:
            print(f"Simplfying {in_length} ... {len(stack)}", end="\r")
        to_add = set()
        to_delete = set()

        for variant in blocks:
            if block == variant:
                continue
            if (
                (block[0][0]-1 == variant[0][0] and block[1] == variant[1] and block[2] == variant[2]) or
                (block[0][1]+1 == variant[0][1] and block[1] == variant[1] and block[2] == variant[2]) or
                (block[0] == variant[0] and block[1][0]-1 == variant[1][0] and block[2] == variant[2]) or
                (block[0] == variant[0] and block[1][1]+1 == variant[1][1] and block[2] == variant[2]) or
                (block[0] == variant[0] and block[1] == variant[1] and block[2][0]-1 == variant[2][0]) or
                (block[0] == variant[0] and block[1] ==
                 variant[1] and block[2][1]+1 == variant[2][1])
            ):

                bigger_block = (
                    (min(block[0][0], variant[0][0]),
                        max(block[0][1], variant[0][1])),
                    (min(block[1][0], variant[1][0]),
                        max(block[1][1], variant[1][1])),
                    (min(block[2][0], variant[2][0]),
                        max(block[2][1], variant[2][1])),
                )

                # print("NEW BLOCK:", block, variant, "-->", bigger_block)
                to_add.add(bigger_block)
                stack.append(bigger_block)
                if block in blocks:
                    to_delete.add(block)
                if variant in blocks:
                    to_delete.add(variant)
                if variant in stack:
                    stack.remove(variant)
                break

        blocks.difference_update(to_delete)
        blocks.update(to_add)
    print(
        f"Simplfying {in_length} --> {len(blocks)}  ({in_length - len(blocks)} blocks less)")

    return blocks


blocks = set()
for i_index, instruction in enumerate(instructions):
    cmd, x_range, y_range, z_range = instruction
    op_block = x_range, y_range, z_range
    if cmd == "on" and i_index == 0:
        blocks.add(op_block)
    else:
        to_delete = []
        to_add = []
        for existing_block in blocks:
            # Splits the existing blocks to the boundries of the new block
            # Replace the old block with the splitted version except the sub-parts that are inside the new block
            splits = split_block(existing_block, op_block)
            to_delete.append(existing_block)
            to_add.extend(
                [new_block for new_block in splits if not check_inclusion(new_block, op_block)])

        blocks.difference_update(to_delete)
        blocks.update(to_add)

        if cmd == "on":
            # Adds the full new block if "on"
            blocks.add(op_block)

    # print("reducing blocks", len(blocks))
    # simplify_blocks(blocks)
    # print("--->", len(blocks))

    print(
        f"After Instruction {i_index} {cmd} (number of blocks {len(blocks)})")


volume = 0
for vol in blocks:
    dx = abs(vol[0][1] - vol[0][0]) + 1
    dy = abs(vol[1][1] - vol[1][0]) + 1
    dz = abs(vol[2][1] - vol[2][0]) + 1
    single_vol = dx * dy * dz
    volume += single_vol

print("Part2", volume)
