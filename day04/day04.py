from __future__ import annotations
from typing import NamedTuple, Dict, List
from dataclasses import dataclass
from collections import defaultdict

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

"""class Pos(NamedTuple):
    x: int
    y: int

@dataclass
class Grid():
    w : int
    h : int
    chars : Dict[Pos, str]
    num_xmas : int = 0




def parse_grid(inp: List[str]) -> Grid:
    h = len(inp)
    w = len(inp[0])
    chars = {}
    for j, line in enumerate(inp):
        for i, char in enumerate(line):
            chars[Pos(i, j)] = char
    return Grid(w, h, chars, 0)
"""


def count_xmas(grid: List[str]) -> int:
    char_map = defaultdict(set)
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            char_map[val].add((r, c))

    #part 1
    counter = 0
    for r, c in char_map['X']:
        for dr, dc in DIRECTIONS:
            for i, char in enumerate('XMAS'):
                if (r + (i * dr), c + (i * dc)) not in char_map[char]:
                    break
            else:
                counter += 1
    return counter

def main():
    with open('day04/day04.txt') as f:
        lines = f.readlines()
    print("part 1:", count_xmas(lines))



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
    lines = RAW.strip().split('\n')
    print("RAW : ", count_xmas(lines))

    main()
