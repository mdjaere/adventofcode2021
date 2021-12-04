import sys
from dataclasses import dataclass

infile = sys.argv[1] if len(sys.argv) > 1 else 'input'
raw_input = open(infile).read()
sections = raw_input.split("\n\n")


@dataclass
class Square:
    value: int = 0
    checked: bool = False


class Board:
    def __init__(self, section):
        self.rows = [[Square(int(c.strip())) for c in row.split()]
                     for row in section.split("\n")]
        self.is_winner = False
        self.winning_number = None

    def add_number(self, number):
        # Add number
        match = False
        for row_idx, row in enumerate(self.rows):
            for col_idx, square in enumerate(row):
                if square.value == number:
                    square.checked = True
                    match = True
                if match:
                    break
            if match:
                break
        # Check board
        if match:
            # check row and column of match
            if all(sq.checked for sq in self.rows[row_idx]) or all(sq.checked for sq in [row[col_idx] for row in self.rows]):
                self.is_winner = True
                self.winning_number = number
        return self.is_winner

    def result(self):
        return sum(sq.value for row in self.rows for sq in row if not sq.checked) * self.winning_number


numbers = [int(c) for c in sections[0].split(",")]
boards = [Board(section) for section in sections[1:]]

winners = []

for number in numbers:
    for board in boards:
        if board.is_winner:
            continue
        board.add_number(number)
        if board.is_winner:
            winners.append(board)


print("Part1:", winners[0].result())
print("Part2:", winners[-1].result())
