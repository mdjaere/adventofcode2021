import sys
from collections import Counter

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
count = Counter(school_0)
count = {i: count[i] if i in count else 0 for i in range(9)}
while day < 256:
    new_count = {i: count[i+1] for i in range(8)}
    new_count[6] += count[0]
    new_count[8] = count[0]
    count = new_count
    day += 1

print(f"Part 2: {sum(count.values())}")
