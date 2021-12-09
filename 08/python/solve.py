import sys
from collections import Counter


infile = sys.argv[1] if len(sys.argv) > 1 else 'input'
input = [[l.split() for l in line.replace("\n", "").split("|")]
         for line in open(infile)]

count = 0
unique_lengths = [2, 3, 4, 7]
for signals, digits in input:
    for digit in digits:
        if len(digit) in unique_lengths:
            count += 1

print(f"Part 1: {count}")

# # PART 2

# pattern_init = [
#     [1, 1, 1, 0, 1, 1, 1],  # 0
#     [0, 0, 1, 0, 0, 1, 0],  # 1
#     [1, 0, 1, 1, 1, 0, 1],  # 2
#     [1, 0, 1, 1, 0, 1, 1],  # 3
#     [0, 1, 1, 1, 0, 1, 0],  # 4
#     [1, 1, 0, 1, 0, 1, 1],  # 5
#     [1, 1, 0, 1, 1, 1, 1],  # 6
#     [1, 0, 1, 0, 0, 1, 0],  # 7
#     [1, 1, 1, 1, 1, 1, 1],  # 8
#     [1, 1, 1, 1, 0, 1, 1]  # 9
# ]

# segments = "ABCFDEG"

# # signals = input[0][0]
# # for row in pattern_init:
# #     print(row, " ", sum(row),  [ signal for signal in signals if len(signal) == sum(row) ] )

# # print()
# # print([sum(col) for col in zip(*pattern)])


# cand_lengths = [sum(p) for p in pattern_init]

# for signals, digits in input[0:1]:

#     pattern = pattern_init.copy()
#     signals = ["".join(sorted(signal)) for signal in signals]
#     digits = ["".join(sorted(digit)) for digit in digits]

#     signal_candidates = []
#     segment_candidates = []
#     solved_signals = {}

#     solved_segments = {}
#     for _ in range(1):

#         char_count = Counter([c for signal in signals for c in signal])

#         for i, row in enumerate(pattern):
#             signal_candidates.append(
#                 [signal for signal in signals if len(signal) == sum(row)]
#             )

#         for i, col in enumerate(zip(*pattern)):
#             segment_candidates.append(
#                 [c for c, count in char_count.items() if count == sum(col)]
#             )

#     # Filter solved

#         for i, signal_cand in enumerate(signal_candidates):
#             if len(signal_cand) == 1:
#                 solved_signals[i] = list(signal_cand)[0]

#         for i, segment_cand in enumerate(segment_candidates):
#             if len(segment_cand) == 1:
#                 solved_segments[segments[i]] = list(segment_cand)[0]

#         print(solved_signals)
#         print(solved_segments)

#     # iteration
#         signal_candidates = [[signal for signal in signals if signal not in solved_signals.values()]
#                              for signals in signal_candidates]
#         print(signal_candidates)
#         segment_candidates = [[segment for segment in segments if segment not in solved_segments.values()]
#                               for segments in segment_candidates]
#         print(segment_candidates)

#         signals = ["".join([c for c in signal if c not in solved_segments.values()])
#                    for signal in signals]

#     # # Debug

#     #     for i, cand in enumerate(signal_candidates):
#     #         print(i, cand - solved_signals)

#     #     for i, segment_cand in enumerate(segment_candidates):
#     #         print(segments[i], segment_cand - solved_segments)
