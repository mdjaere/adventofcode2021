import sys
from collections import OrderedDict
import copy

infile = sys.argv[1] if len(sys.argv) > 1 else 'input'
raw_input = open(infile).read()
sections = raw_input.split("\n\n")

numbers = [int(c) for c in sections[0].split(",")]
boards = [[[{"value": int(c.strip()), "checked": False} for c in row.split()]
           for row in board.split("\n")]for board in sections[1:]]


def is_winner(board):
    for row in board:
        if all(sq["checked"] for sq in row):
            return True
    for column in zip(*board):
        if all(sq["checked"] for sq in column):
            return True
    return False


winners = OrderedDict()

for number in numbers:
    for board_idx, board in enumerate(boards):
        for row in board:
            for square in row:
                if square["value"] == number:
                    square["checked"] = True
        if is_winner(board):
            if not board_idx in winners:
                winners[board_idx] = {
                    "board": copy.deepcopy(board), "number": number}

winner_list = list(winners.values())
first = winner_list[0]
last = winner_list[-1]


def calc_result(item):
    return sum(sq["value"]
               for row in item["board"] for sq in row if not sq["checked"]) * item["number"]


print("Part1:", calc_result(first))
print("Part2:", calc_result(last))
