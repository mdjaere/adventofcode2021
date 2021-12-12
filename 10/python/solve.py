import sys
import statistics as st

infile = sys.argv[1] if len(sys.argv) > 1 else 'input'

lines = [line.strip() for line in open(infile)]

o_tags = "([{<"
c_tags = ")]}>"


def parse(data, missing_tags=None, level=0):
    if missing_tags == None:
        missing_tags = []
    while data:
        if data[0] in o_tags:
            closing_tag = c_tags[o_tags.index(data[0])]
            data = parse(data[1:], missing_tags, level+1)
            if data == None:  # No more? It's incomplete!
                missing_tags.append(closing_tag)
                if level == 0:
                    return "".join(missing_tags)
                else:
                    return None
            elif data[0] == closing_tag:  # Found a pair? Continue on this level
                data = data[1:]
                continue
            elif data[0] != closing_tag:
                raise SyntaxError(data[0])  # Unexpected character, abort
        else:
            return data  # If it's not an opening tag, pass if back down


first_corrupts = []
completions = []
for line in lines:
    # print("START", line)
    try:
        auto_completion = parse(line)
        completions.append(auto_completion)
    except SyntaxError as err:
        first_corrupts.append(str(err))

corrupt_score = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}

r1 = sum(first_corrupts.count(score_type) * score_value for score_type,
         score_value in corrupt_score.items())

print(f"Part1: {r1}")

autocmplete_score = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}

r2_sums = []
for com in completions:
    s = 0
    for c in com:
        s *= 5
        s += autocmplete_score[c]
    r2_sums.append(s)

median = st.median(r2_sums)
print("Part2:", median)
