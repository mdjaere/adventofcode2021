import sys
from collections import Counter, deque

infile = sys.argv[1] if len(sys.argv) > 1 else 'input'
school_0 = [int(x) for x in open(infile).read().split(",")]


school = school_0.copy()
day = 0
while day < 80:
    spawn = 0
    for i, fish_age in enumerate(school):
        if fish_age == 0:
            spawn += 1
            school[i] = 6
        else:
            school[i] = fish_age - 1
    school = school + ([8] * spawn)
    day += 1

print(f"Part 1: {len(school)}")

day = 0
counter = Counter(school_0)
count = deque(counter[i] if i in counter else 0 for i in range(9))
for _ in range(256):
    count.rotate(-1)
    count[6] += count[8]

print(f"Part 2: {sum(count)}")
