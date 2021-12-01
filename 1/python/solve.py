import fileinput

nums = [int(line.strip()) for line in fileinput.input()]

ups = 0
last = nums[0]
for num in nums[1:]:
    if num > last:
        ups += 1
    last = num
print(ups)

