from __future__ import annotations
from typing import NamedTuple, Dict, List
from dataclasses import dataclass

DIRECTIONS = [
    (-1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
    (1, 0),
    (1, -1),
    (0, -1),
    (-1, -1)
]

class Pos(NamedTuple):
    x: int
    y: int

@dataclass
class Grid():
    w : int
    h : int
    chars : Dict[Pos, str]
    num_xmas : int = 0


    def xmas_count_per_position(self, pos: Pos) -> bool:
        # left-to-right
        for i in range(self.w):
            for j in range(self.h - 1):
                if not self.chars[Pos(i, j)] == 'X':
                    continue
                else:
                    print((i, j), self.chars[Pos(i, j)])
                    if (self.chars[Pos(i, j+1)] == 'M'
                        and self.chars[Pos(i, j+2)] == 'A'
                        and self.chars[Pos(i, j+3)] == 'S'):
                        self.num_xmas += 1
        print(f"left-to-right {self.num_xmas=}")
        # right-to-left
        for i in range(self.w):
            for j in range(2, self.h - 1):
                if not self.chars[Pos(i, j)] == 'X':
                    continue
                else:
                    if (self.chars[Pos(i, j-1)] == 'M'
                        and self.chars[Pos(i, j-2)] == 'A'
                        and self.chars[Pos(i, j-3)] == 'S'):
                        self.num_xmas += 1
        print(f"{self.num_xmas=}")
        # top-to-bottom
        for i in range(self.w - 1):
            for j in range(self.h):
                if not self.chars[Pos(i, j)] == 'X':
                    continue
                else:
                    if (self.chars[Pos(i+1, j)] == 'M'
                        and self.chars[Pos(i+2, j)] == 'A'
                        and self.chars[Pos(i+3, j)] == 'S'):
                        self.num_xmas += 1
        print(f"{self.num_xmas=}")
        # bottom-to-top
        for i in range(1, self.w - 1):
            for j in range(self.h - 1):
                if not self.chars[Pos(i, j)] == 'X':
                    continue
                else:
                    if (self.chars[Pos(i-1, j)] == 'M'
                        and self.chars[Pos(i-2, j)] == 'A'
                        and self.chars[Pos(i-3, j)] == 'S'):
                        self.num_xmas += 1
        print(f"{self.num_xmas=}")
        # diagonal top-left to bottom-right
        for i in range(self.w - 1):
            for j in range(self.h - 1):
                if not self.chars[Pos(i, j)] == 'X':
                    continue
                else:
                    if (self.chars[Pos(i+1, j+1)] == 'M'
                        and self.chars[Pos(i+2, j+2)] == 'A'
                        and self.chars[Pos(i+3, j+3)] == 'S'):
                        self.num_xmas += 1
        print(f"{self.num_xmas=}")
        # diagonal top-right to bottom-left
        for i in range(self.w - 1):
            for j in range(1, self.h - 1):
                if not self.chars[Pos(i, j)] == 'X':
                    continue
                else:
                    if (self.chars[Pos(i+1, j-1)] == 'M'
                        and self.chars[Pos(i+2, j-2)] == 'A'
                        and self.chars[Pos(i+3, j-3)] == 'S'):
                        self.num_xmas += 1
        print(f"{self.num_xmas=}")
        # diagonal bottom-left to top-right
        for i in range(1, self.w - 1):
            for j in range(self.h - 1):
                if not self.chars[Pos(i, j)] == 'X':
                    continue
                else:
                    if (self.chars[Pos(i-1, j+1)] == 'M'
                        and self.chars[Pos(i-2, j+2)] == 'A'
                        and self.chars[Pos(i-3, j+3)] == 'S'):
                        self.num_xmas += 1
        print(f"{self.num_xmas=}")
        # diagonal bottom-right to top-left
        for i in range(2, self.w - 1):
            for j in range(2, self.h - 1):
                if not self.chars[Pos(i, j)] == 'X':
                    continue
                else:
                    if (self.chars[Pos(i-1, j-1)] == 'M'
                        and self.chars[Pos(i-2, j-2)] == 'A'
                        and self.chars[Pos(i-3, j-3)] == 'S'):
                        self.num_xmas += 1
        print(f"{self.num_xmas=}")




def parse_grid(inp: List[str]) -> Grid:
    h = len(inp)
    w = len(inp[0])
    chars = {}
    for j, line in enumerate(inp):
        for i, char in enumerate(line):
            chars[Pos(i, j)] = char
    return Grid(w, h, chars, 0)


def main():
    with open('day04/day04.txt') as f:
        lines = f.readlines()
    grid = parse_grid(lines)
    #print(grid)
    for pos in grid.chars.keys():
        #print(f"{pos=} ==> {grid.num_xmas=}")
        grid.xmas_count_per_position(pos)





if __name__ == "__main__":
    RAW="""
....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX"""

    grid = parse_grid(RAW.strip().split('\n'))

    for pos in grid.chars.keys():
        grid.xmas_count_per_position(pos)
        # print(f"{pos=} ==> {grid.chars[pos]=}")

    #main()
