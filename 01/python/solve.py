import fileinput
data = [int(line.strip()) for line in fileinput.input()]

ups = sum(1 for i in range(len(data)-1) if data[i+1] - data[i] > 0)
print(f"Part 1: {ups}")

tri_ups = sum([1 for i in range(len(data)-3) if data[i+3] - data[i] > 0])
print(f"Part 2: {tri_ups}")
