from typing import NamedTuple, List, Tuple, Iterator
from dataclasses import dataclass
from itertools import cycle
from collections import OrderedDict
from pprint import pprint

DIRECTIONS = OrderedDict([
    ("UP", (0, -1)),
    ("RIGHT", (1, 0)),
    ("DOWN", (0, 1)),
    ("LEFT", (-1, 0))]
)
class Pos(NamedTuple):
    x: int
    y: int


@dataclass
class Grid():
    obstacles: List[Pos] = None
    starting_pos: Pos = None
    current_pos: Pos = None
    current_dir: Tuple[int, int] = None
    dir_gen : Iterator = None
    guard_positions: List[Pos] = None
    guard_outside_grid : bool = None
    x_min : int = None
    x_max : int = None
    y_min : int = None
    y_max : int = None
    new_obstacles: List[Pos] = None

    def parse(self, raw: str) -> None:
        self.obstacles = []
        self.guard_positions = []
        for y, line in enumerate(raw.split("\n")):
            self.y_min = 0
            self.y_max = len(raw.split("\n")) - 1
            for x, char in enumerate(line):
                self.x_min = 0
                self.x_max = len(line) - 1
                if char == "#":
                    self.obstacles.append(Pos(x, y))
                if char in ("^>v<"):
                    self.starting_pos = Pos(x, y)
                    self.current_pos = Pos(x, y)
                    self.guard_positions.append(Pos(x, y))
                    self.guard_outside_grid = False
                    if char == "^":
                        self.current_dir = DIRECTIONS["UP"]
                    elif char == ">":
                        self.current_dir = DIRECTIONS["RIGHT"]
                    elif char == "v":
                        self.current_dir = DIRECTIONS["DOWN"]
                    else:
                        self.current_dir = DIRECTIONS["LEFT"]


    def reset_directions(self) -> OrderedDict:
        """reset DIRECTIONS so that when the generator is called again it starts
        from the correct value and not always UP
        e.g. current_dir = (0, 1)"""

        current_dir_idx = list(DIRECTIONS.values()).index(self.current_dir)
        start = list(DIRECTIONS)[current_dir_idx + 1:]
        rest = list(DIRECTIONS)[:current_dir_idx + 1]
        new_order = start + rest
        new_directions = OrderedDict([(el, DIRECTIONS[new_order[i]]) for i, el in enumerate(new_order)])
        self.dir_gen = cycle([el for el in new_directions])


    def move(self) -> Pos:
        dx, dy = self.current_dir
        new_pos = Pos(self.current_pos.x + dx, self.current_pos.y + dy)
        if new_pos in self.obstacles:
            new_dir = next(self.dir_gen)
            self.current_dir = DIRECTIONS[new_dir]
            # print(f"Guard faced an obstacle, changed direction to {self.current_dir}")
            return
        if not (self.x_min <= new_pos.x <= self.x_max and self.y_min <= new_pos.y <= self.y_max):
            self.guard_outside_grid = True
            # print("Guard is outside the grid")
            return
        # print(f"Guard moves from {self.current_pos} at {new_pos}")
        self.current_pos = new_pos
        self.guard_positions.append(new_pos)

    def add_obstacle(self, pos: Pos) -> None:
        self.obstacles.append(pos)





RAW = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

grid = Grid()
grid.parse(RAW)
grid.reset_directions()
while grid.guard_outside_grid is False:
    grid.move()
assert len(set(grid.guard_positions)) == 41

def main():
    with open("day06.txt") as f:
        raw = f.read()
    grid = Grid()
    grid.parse(raw)
    grid.reset_directions()
    while grid.guard_outside_grid is False:
        grid.move()
    print(f"part 1 : {len(set(grid.guard_positions))}, {grid.starting_pos=}")

    grid_2 = Grid()
    grid_2.parse(raw)
    grid_2.reset_directions()
    grid_2.new_obstacles = list(set(grid.guard_positions))
    grid_2.new_obstacles.remove(grid.starting_pos) #can't be placed at the guard's starting position

    for obstacle in grid_2.new_obstacles:
        grid_2.obstacles.append(obstacle)
        while grid_2.guard_outside_grid is False:
            grid_2.move()
    print(f"part 2 : {len(set(grid.guard_positions))}")

if __name__ == "__main__":
    main()
