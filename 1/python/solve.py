import fileinput
nums = [int(line.strip()) for line in fileinput.input()]

ups = 0
last = nums[0]
for num in nums[1:]:
    if num > last:
        ups += 1
    last = num
print(f"Part 1: {ups}")


tri_ups = 0
last = sum(nums[0:3])
for i in range(len(nums)):
    window = nums[1+i:4+i]
    if len(window) < 3:
        break
    tri_sum = sum(window)
    if tri_sum > last:
        tri_ups += 1
    last = tri_sum
print(f"Part 2: {tri_ups}")
