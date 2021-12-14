import sys
import os
from collections import Counter, defaultdict

inpath = sys.argv[1] if len(sys.argv) > 1 else 'input'

data_start, raw_instructions = open(inpath).read().split("\n\n")
instructions = dict([line.split(" -> ")
                    for line in raw_instructions.split("\n")])

# Part 1

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

combination_map = {k: [k[0]+v, v+k[1]] for k, v in instructions.items()}
pairs_count = Counter([data_start[i] + data_start[i+1]
                      for i in range(len(data_start)-1)])

for i in range(40):
    new_count = defaultdict(lambda: 0)
    for pair, count in pairs_count.items():
        for k in combination_map[pair]:
            new_count[k] += count
    pairs_count = new_count

char_count = defaultdict(lambda: 0)
for char_pair, count in pairs_count.items():
    char_count[char_pair[0]] += count
char_count[data_start[-1]] += 1  # Also count the very last character

freq_data = sorted(char_count.values())
print("Part2:", freq_data[-1] - freq_data[0])
