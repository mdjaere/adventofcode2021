import fileinput

data = [line.strip() for line in fileinput.input()]

def max_string(data):
    sums = [0]*len(data[0])
    for i in range(len(data[0])):
        for item in data:
            sums[i] = sums[i] + int(item[i])
    max_str = "".join(["1" if x >= len(data) / 2 else "0" for x in sums])
    return max_str

def inverse_bit_string(bit_string):
    return "".join(["1" if x == "0" else "0" for x in bit_string])

gamma_string = max_string(data)
epsilon_string = inverse_bit_string(gamma_string)

gamma = int(gamma_string, 2)
epsilon = int(epsilon_string, 2)
print(f"Part1: {gamma * epsilon}")

# Part 2

oxygen_data = data.copy()
for i in range(len(oxygen_data[0])):
    new_aim = max_string(oxygen_data)
    oxygen_data = [item for item in oxygen_data if item[i] == new_aim[i]]
    if len(oxygen_data) == 1:
        break

oxygen_rating = int(oxygen_data[0], 2)

scrubber_data = data.copy()
for i in range(len(scrubber_data[0])):
    new_aim = inverse_bit_string(max_string(scrubber_data))
    scrubber_data = [item for item in scrubber_data if item[i] == new_aim[i]]
    if len(scrubber_data) == 1:
        break

scrubber_rating = int(scrubber_data[0], 2)

print(f"Part2: { oxygen_rating * scrubber_rating }")
