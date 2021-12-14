import sys
import os
from collections import Counter, defaultdict

inpath = sys.argv[1] if len(sys.argv) > 1 else 'input'

data_start, raw_instructions = open(inpath).read().split("\n\n")
instructions = dict([line.split(" -> ")
                    for line in raw_instructions.split("\n")])

base = os.path.join(".", "tmp", inpath)

os.makedirs(base, exist_ok=True)

with open(os.path.join(base, "0"), "w") as writefile:
    for x in data_start:
        writefile.writelines(x)

for i in range(10):
    with open(os.path.join(base, str(i)), "r") as readfile:
        with open(os.path.join(base, str(i+1)), "w") as writefile:
            data_0 = readfile.read(1)
            data_1 = readfile.read(1)
            writefile.write(data_0)
            while data_1:
                code = data_0 + data_1
                writefile.write(instructions[code] + data_1)
                data_0, data_1 = data_1, readfile.read(1)

count = defaultdict(lambda: 0)

with open(os.path.join(base, "10")) as count_file:
    c = count_file.read(1)
    while c:
        count[c] += 1
        c = count_file.read(1)

freq_data = sorted(count.values())
print("Part1:", freq_data[-1] - freq_data[0])

# Part 2

combination_map = {}
for i in instructions.items():
    k, v = i
    combination_map[k] = k[0]+v, v+k[1]

pairs_count = defaultdict(lambda: 0)
for i in range(len(data_start)-1):
    pairs_count[data_start[i] + data_start[i+1]] += 1

for i in range(40):
    new_count = defaultdict(lambda: 0)
    for in_key, in_count in pairs_count.items():
        for k in combination_map[in_key]:
            new_count[k] += in_count
    pairs_count = new_count

c_count = defaultdict(lambda: 0)
for c_pair, count in pairs_count.items():
    c_count[c_pair[0]] += count
c_count[data_0[-1]] += 1

freq_data = sorted(c_count.values())
print("Part2:", freq_data[-1] - freq_data[0])
