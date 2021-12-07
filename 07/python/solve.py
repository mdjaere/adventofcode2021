import sys
import statistics as st

infile = sys.argv[1] if len(sys.argv) > 1 else 'input'
input = [int(x) for x in open(infile).read().split(",")]

m = round(st.median(input))
r1 = sum(abs(i-m) for i in input)
print("Part1:", r1)

def gauss_summation(n):
    return (n*(n+1))/2

r2 = min(sum(gauss_summation(abs(i-x)) for i in input) for x in range(min(input), max(input)))
print("Part1:", r2)
