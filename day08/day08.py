from typing import NamedTuple, List, Dict
from itertools import combinations
from collections import defaultdict


class Point(NamedTuple):
    x: int
    y: int

def parse(raw: str) -> Dict[str, List[Point]]:
    char_to_points = {}
    lines = raw.strip().split("\n")
    y_min = 0
    y_max = len(lines)
    x_min = 0
    x_max = len(lines[0])
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == ".":
                pass
            else:
                if char not in char_to_points:
                    char_to_points[char] = []
                char_to_points[char].append(Point(x,y))
    return char_to_points, x_min, x_max, y_min, y_max

def place_antinodes(char_to_points : Dict[str, List[Point]],
                    x_min: int,
                    x_max: int,
                    y_min: int,
                    y_max: int):
    early_stop = 0
    antinodes = {}
    all_combinations = {}

    # {'0': [(Point(x=8, y=1), Point(x=5, y=2)) ..., 'A': [(Point(x=6, y=5), Point(x=8, y=8))...}
    for k, v in char_to_points.items():
        comb = list(combinations(v, 2))
        all_combinations[k] = comb


    for k, v in all_combinations.items():
        # (Point(x=8, y=1), Point(x=5, y=2)
        # if early_stop > 3:
        #         break
        for pair in v:
            dx1 = pair[0].x - pair[1].x
            dy1 = pair[0].y - pair[1].y
            dx2 = - dx1
            dy2 = - dy1

            # first antinode
            if x_min <= pair[0].x + dx1 <= x_max  and  y_min <= pair[0].y + dy1 <= y_max:
                antinode = Point(pair[0].x + dx1, pair[0].y + dy1)
                if k not in antinodes:
                    antinodes[k] = []
                antinodes[k].append(antinode)
                early_stop += 1
                # print(f"First antinode {k=}, {pair=}, {dx1=}, {dy1=}, {antinode=} ")

            # symetric antinode
            if x_min <= pair[1].x + dx2 <= x_max  and  y_min <= pair[1].y + dy2 <= y_max:
                antinode = Point(pair[1].x + dx2, pair[1].y + dy2)
                if k not in antinodes:
                    antinodes[k] = []
                antinodes[k].append(antinode)
                early_stop += 1
                # print(f"Symetric antinode {k=}, {pair=}, {dx2=}, {dy2=}, {antinode=} ")
    return antinodes

def compute_sum(antinodes: Dict[str, List[Point]]) -> int:
    res = set()
    for v in antinodes.values():
        for el in v:
            res.add(el)
    return len(res)

RAW_1 = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

# char_to_points, x_min, x_max, y_min, y_max = parse(RAW_1)
# print(f"TEST {char_to_points=}")
# antinodes = place_antinodes(char_to_points, x_min, x_max, y_min, y_max)
# print(f"TEST RAW: {compute_sum(antinodes)=}")

RAW_2 = """
......#....#
...#....0...
....#0....#.
..#....0....
....0....#..
.#....A.....
...#........
#......#....
........A...
.........A..
..........#.
..........#."""

def main():
    with open("day08.txt") as f:
        raw = f.read().strip()
    char_to_points, x_min, x_max, y_min, y_max = parse(raw)
    print(f"{len(char_to_points)=}")
    print(f"{[{k : len(v)} for k, v in char_to_points.items()][:5]=}")
    print(f"{x_min=}, {x_max=}, {y_min=}, {y_max=}")
    antinodes = place_antinodes(char_to_points, x_min, x_max, y_min, y_max)
    print(f"{antinodes.keys()=}")
    print(f"{len(antinodes)=}")
    print(f"{antinodes.values()=}")

    print(f"Part 1 : {compute_sum(antinodes)=}")


if __name__ == "__main__":
    main()
