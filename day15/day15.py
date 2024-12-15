from typing import NamedTuple, List, Tuple
from itertools import zip_longest

DIRECTIONS = {"^": (0, -1), "v": (0, 1), "<": (-1, 0), ">": (1, 0)}


class P(NamedTuple):
    x: int
    y: int


class Wharehouse(NamedTuple):
    width: int
    length: int
    robot: P
    boxes: List[P]
    walls: List[P]
    free: List[P]


class WharehouseTwice(NamedTuple):
    width: int
    length: int
    robot: P
    boxes: List[Tuple[P, P]]
    walls: List[P]
    free: List[P]


def parse(raw: str) -> Tuple[Wharehouse, str]:
    """Parse the input string to return a wharehouse <Wharehouse> object and the moves <str> to be made"""
    wharehouse, moves = raw.strip().split("\n\n")
    moves = "".join([m for m in moves if m != "\n"])
    width, length = None, None
    boxes, walls, free = [], [], []
    for y, line in enumerate(wharehouse.splitlines()):
        if not width:
            width = len(wharehouse.splitlines())
        if not length:
            length = len(line)
        for x, char in enumerate(line):
            if char == "@":
                robot = P(x, y)
            elif char == "O":
                boxes.append(P(x, y))
            elif char == "#":
                walls.append(P(x, y))
            elif char == ".":
                free.append(P(x, y))
            else:
                raise ValueError(f"Unexpected character {char}")
    return Wharehouse(width, length, robot, boxes, walls, free), moves


def swap_box_free(
    w: Wharehouse,
    char: str,
    boxes_ahead: List[P],
    free_ahead: List[P],
    robot: P,
    new_robot: P,
) -> Wharehouse:
    """When the robot finds a box, move it to the next closest free space. Update current box position with a freespace
    Takes into consideration if we are going in positive direction(>v) or negative(<^)
    Returns a new wharehouse with the robot and the box in their new positions"""

    boxes_ahead, free_ahead = sorted(boxes_ahead), sorted(free_ahead)
    if char in ">v":
        box_pop, free_pop = boxes_ahead[0], free_ahead[0]
    elif char in "<^":
        box_pop, free_pop = boxes_ahead[-1], free_ahead[-1]

    new_boxes, new_free = w.boxes.copy(), w.free.copy()

    new_boxes.remove(box_pop)
    new_boxes.append(free_pop)

    new_free.remove(free_pop)
    new_free.append(robot)  # old robot position is now free
    return Wharehouse(w.width, w.length, new_robot, new_boxes, w.walls, new_free)


def move(char: str, w: Wharehouse) -> Wharehouse:
    """Check the new position for the robot
    - return same wharehouse if there is a wall
    - return new wharehouse if there is an empty space, with the robot in its new position
    - if there is a box
        - if the box can be moved, return the new wharehouse with the robot and the box in its new positions
        - otherwise return the same wharehouse"""

    r = w.robot
    dx, dy = DIRECTIONS[char]
    new_robot = P(r.x + dx, r.y + dy)

    if new_robot in w.walls:
        return w
    elif new_robot in w.free:
        new_free = w.free.copy()
        new_free.remove(new_robot)
        new_free.append(r)
        return Wharehouse(w.width, w.length, new_robot, w.boxes, w.walls, new_free)
    elif new_robot in w.boxes:

        #### check what is ahead
        boxes_ahead, free_ahead = [], []
        x_range = w.width - r.x if char in ">v" else r.x
        y_range = w.length - r.y if char in ">v" else r.y
        for px, py in zip_longest(
            range(1, x_range), range(1, y_range)
        ):  # start 1 to avoid checking the robot's current position
            if px == None:
                px = py  # zip longest sends None, force value as we move along the y axis
            if py == None:
                py = px  # zip longest sends None, force value as we move along the x axis
            pos = P(r.x + dx * px, r.y + dy * py)

            if pos in w.walls:
                break
            elif pos in w.boxes:
                boxes_ahead.append(pos)
            elif pos in w.free:
                free_ahead.append(pos)
            else:
                raise ValueError(f"Unexpected thing at position {pos}")

        #### case by case solution
        if not free_ahead:
            return w
        else:
            return swap_box_free(w, char, boxes_ahead, free_ahead, r, new_robot)


def w_print(w: Wharehouse) -> None:
    """Print the wharehouse in teh terminal"""
    for y in range(w.length):
        for x in range(w.width):
            if P(x, y) == w.robot:
                print("@", end="")
            elif P(x, y) in w.boxes:
                print("O", end="")
            elif P(x, y) in w.walls:
                print("#", end="")
            elif P(x, y) in w.free:
                print(".", end="")
        print(end="\n")
    print(end="\n")


def gps(w: Wharehouse) -> int:
    """ "Calculate the GPS value of the wharehouse"""
    return sum([box.y * 100 + box.x for box in w.boxes])


def build_twice_map(raw: str) -> List[List[str]]:
    """Build the map of the wharehouse with the boxes and the robot"""
    wharehouse_map = raw.split("\n\n")[0]
    str_map = []
    for line in wharehouse_map.strip().splitlines():
        new_line = []
        for char in line:
            if char == "@":
                new_line.append("@")
            elif char == "O":
                new_line.append("[")
                new_line.append("]")
            elif char == ".":
                new_line.append(".")
                new_line.append(".")
            elif char == "#":
                new_line.append("#")
                new_line.append("#")
            else:
                raise ValueError(f"Unexpected character {char}")
        str_map.append(new_line)
    return str_map


def get_wharehouse_twice(str_map: List[List[str]]) -> WharehouseTwice:
    """Get the wharehouse object for the twice map"""
    width, length = len(str_map[0]), len(str_map)
    robot = None
    boxes, walls, free = [], [], []
    for y, line in enumerate(str_map):
        for x, char in enumerate(line):
            if char == "@":
                robot = P(x, y)
            elif char == "[":
                boxes.append((P(x, y), P(x + 1, y)))
            elif char == "#" and P(x + 1, y) not in [w2 for (w1, w2) in walls]:
                walls.append(P(x, y))
                walls.append(P(x + 1, y))
            elif char == "." and P(x + 1, y) not in [w2 for (w1, w2) in free]:
                free.append(P(x, y))
                free.append(P(x +1 , y))
    return WharehouseTwice(width, length, robot, boxes, walls, free)

def w_twice_print(w: WharehouseTwice) -> None:
    """Print the wharehouse in teh terminal"""
    for y in range(w.length):
        for x in range(w.width):
            if P(x, y) == w.robot:
                print("@", end="")
            elif (P(x, y), P(x+1, y)) in w.boxes:
                print("[]", end="")
            elif P(x, y) in w.walls:
                print("#", end="")
            elif P(x, y) in w.free:
                print(".", end="")
        print(end="\n")
    print(end="\n")

RAW = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

RAW_2 = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""

RAW_2_final = """
##########
#.O.O.OOO#
#........#
#OO......#
#OO@.....#
#O#.....O#
#O.....OO#
#O.....OO#
#OO....OO#
##########\n\n<"""

def run(name:str, raw: str) -> None:
    wharehouse, moves = parse(raw)
    for m in moves:
        wharehouse = move(m, wharehouse)
    gps_value = gps(wharehouse)
    print(f"{name} : ", gps_value)
    w_print(wharehouse)
    print("_" * 60)
    return  gps_value

if __name__ == "__main__":
    assert run("test", RAW) == 2028
    assert run("test 2", RAW_2)  == 10092


    with open("day15.txt") as f:
        data = f.read()
    run("part1", data)

    print("part2")
    str_map = build_twice_map(RAW_2)
    wharehouse_twice = get_wharehouse_twice(str_map)
    w_twice_print(wharehouse_twice)
