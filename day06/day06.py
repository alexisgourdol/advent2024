from typing import NamedTuple, List, Tuple, Iterator, Set
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

class PosGuard(NamedTuple):
    x: int
    y: int
    d: tuple

@dataclass
class Grid():
    obstacles: List[Pos] = None
    starting_pos: PosGuard = None
    starting_dir: Tuple[int, int] = None
    current_pos: PosGuard = None
    current_dir: Tuple[int, int] = None
    dir_gen : Iterator = None
    guard_positions: Set[PosGuard] = None
    guard_outside_grid : bool = None
    x_min : int = None
    x_max : int = None
    y_min : int = None
    y_max : int = None
    new_obstacles: Set[Pos] = None
    loop_counter : int = None

    def parse(self, raw: str) -> None:
        self.obstacles = []
        self.guard_positions = set()
        for y, line in enumerate(raw.split("\n")):
            self.y_min = 0
            self.y_max = len(raw.split("\n")) - 1
            for x, char in enumerate(line):
                self.x_min = 0
                self.x_max = len(line) - 1
                if char == "#":
                    self.obstacles.append(Pos(x, y))
                if char in ("^>v<"):
                    self.guard_outside_grid = False
                    if char == "^":
                        self.current_dir = DIRECTIONS["UP"]
                    elif char == ">":
                        self.current_dir = DIRECTIONS["RIGHT"]
                    elif char == "v":
                        self.current_dir = DIRECTIONS["DOWN"]
                    else:
                        self.current_dir = DIRECTIONS["LEFT"]
                    self.starting_pos = PosGuard(x, y, self.current_dir )
                    self.starting_dir = self.current_dir
                    self.current_pos = PosGuard(x, y, self.current_dir)
                    self.guard_positions.add(PosGuard(x, y, self.current_dir))


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


    def move(self) -> None:
        dx, dy = self.current_dir
        new_pos_with_dir = PosGuard(self.current_pos.x + dx, self.current_pos.y + dy, self.current_dir)
        new_pos = Pos(new_pos_with_dir.x, new_pos_with_dir.y)
        if new_pos in self.obstacles:
            new_dir = next(self.dir_gen)
            self.current_dir = DIRECTIONS[new_dir]
            print(f"Guard faced an obstacle, changed direction to {self.current_dir}")
            return
        if not (self.x_min <= new_pos.x <= self.x_max and self.y_min <= new_pos.y <= self.y_max):
            self.guard_outside_grid = True
            print("Guard is outside the grid")
            return
        print(f"Guard moves from {self.current_pos} at {new_pos_with_dir}")
        self.current_pos = new_pos_with_dir
        self.guard_positions.add(new_pos_with_dir)

    def add_obstacles_and_simulate(self) -> None:
        self.loop_counter  = 0
        for obstacle in self.new_obstacles:
            #reset state
            self.guard_positions  = set()
            self.guard_positions.add(self.starting_pos)
            self.current_dir = self.starting_dir
            self.current_pos = self.starting_pos
            self.reset_directions()

            # add obstacle
            self.guard_outside_grid = False
            self.obstacles.append(obstacle)

            while self.guard_outside_grid is False:
                pos_before_move = self.current_pos
                self.move()
                pos_after_move = self.current_pos

                # if position and directions have already been registered, break out of the loop
                # BUG => this is always True as the move() method adds the new position to the set
                if (
                    self.current_pos in self.guard_positions.difference(pos_before_move).difference(pos_after_move)
                    ):
                    print(f"{self.current_pos in self.guard_positions=}")
                    self.loop_counter += 1
                    break
            # remove obstacle and try with the next
            self.obstacles.remove(obstacle)



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
pprint(grid.__dict__)
while grid.guard_outside_grid is False:
    grid.move()

# remove the direction tracking for part 1
res = set([(Pos(pos.x, pos.y)) for pos in grid.guard_positions])
assert len(res) == 41

grid_2 = Grid()
grid_2.parse(RAW)
grid_2.reset_directions()
grid_2.new_obstacles = set([
    (Pos(pos.x, pos.y))
    for pos in grid.guard_positions
    if pos != grid.starting_pos     #can't be placed at the guard's starting position
])

grid_2.add_obstacles_and_simulate()
print(f"test part 2 : {grid_2.loop_counter=}")



def main():
    with open("day06.txt") as f:
        raw = f.read()

    # part 1
    grid = Grid()
    grid.parse(raw)
    grid.reset_directions()
    while grid.guard_outside_grid is False:
        grid.move()
    res = set([(Pos(pos.x, pos.y)) for pos in grid.guard_positions])
    print(f"part 1 : {len(res)=}")

    # part 2 : new Grid will all candidate positions for obstacles
    # added directions tracking in the PosGuard class
    grid_2 = Grid()
    grid_2.parse(raw)
    grid_2.reset_directions()
    grid_2.new_obstacles = set([
        (Pos(pos.x, pos.y))
        for pos in grid.guard_positions
        if pos != grid.starting_pos     #can't be placed at the guard's starting position
    ])

    grid_2.add_obstacles_and_simulate()
    print(f"part 2 : {grid_2.loop_counter=}")

if __name__ == "__main__":
    ...
#   main()
