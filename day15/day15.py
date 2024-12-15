from typing import NamedTuple, List, Tuple
from pprint import pprint
DIRECTIONS = {
        '^': (0, -1),
        'v': (0, 1),
        '<': (-1, 0),
        '>': (1, 0)
    }
class P(NamedTuple):
    x: int
    y: int


class Wharehouse(NamedTuple):
    width : int
    length : int
    robot_pos: P
    boxes_pos: List[P]
    walls_pos: List[P]



def parse(raw: str)-> Tuple[Wharehouse, str]:
    wharehouse_raw, moves_raw = raw.strip().split('\n\n')
    moves = "".join([m for m in moves_raw if m != '\n'])
    width = None
    length = None
    boxes_pos = []
    walls_pos = []
    for y, line in enumerate(wharehouse_raw.splitlines()):
        if not width:
            width = len(wharehouse_raw.splitlines())
        if not length:
            length = len(line)
        for x, char in enumerate(line):
            if char == '@':
                robot_pos = P(x, y)
            elif char == 'O':
                boxes_pos.append(P(x, y))
            elif char == '#':
                walls_pos.append(P(x, y))
            else:
                continue
    return Wharehouse(width, length, robot_pos, boxes_pos, walls_pos), moves

def move(char: str, wharehouse: Wharehouse) -> Wharehouse:
    """Check the new position for the robot
        - return same wharehouse if there is a wall
        - return new wharehouse if there is an empty space, with the robot in its new position
        - if there is a box
            - if the box can be moved, return the new wharehouse with the robot and the box in its new positions
            - otherwise return the same wharehouse"""

    robot = wharehouse.robot_pos
    dx, dy = DIRECTIONS[char]
    new_robot = P(robot.x + dx, robot.y  + dy)

    if new_robot in wharehouse.walls_pos:
        # print("  **  Wall encountered")
        return wharehouse

    elif new_robot not in (wharehouse.walls_pos + wharehouse.boxes_pos):
        # print(f"  **  Empty space encountered {new_robot=}")
        return Wharehouse(
           wharehouse.width,
           wharehouse.length,
           new_robot,
           wharehouse.boxes_pos,
           wharehouse.walls_pos)

    elif new_robot in wharehouse.boxes_pos:
        boxes_ahead = []
        empty_ahead = []
        new_boxes = []
        # print(f"  **  Box encountered {new_robot=}")
        for px, py in zip(
            range(1, wharehouse.width - robot.x),
            range(1, wharehouse.length - robot.y)
            ):
            pos = P(robot.x + dx * px, robot.y + dy * py)

            if (pos.y in (0, wharehouse.length) or pos.x in (0, wharehouse.width)):
                # print(f"    **  Wall encountered for checked position:{pos=}")
                break
            if pos in wharehouse.boxes_pos:
                # print(f"    **  Box appended:{pos=}")
                boxes_ahead.append(pos)
            if pos not in (wharehouse.walls_pos + wharehouse.boxes_pos ):
                # print(f"    **  Empty pos detected:{pos=}")
                empty_ahead.append(pos)

        # looping over boxes ahead approach
        for box in boxes_ahead:
            if P(box.x + dx, box.y + dy) in empty_ahead:
                new_boxes = wharehouse.boxes_pos.copy()
                new_boxes.remove(box)
                new_boxes.append(P(box.x + dx, box.y + dy))
                print(f"  **  Box moved: \n{new_boxes} ")
                return Wharehouse(
                    wharehouse.width,
                    wharehouse.length,
                    new_robot,
                    new_boxes,
                    wharehouse.walls_pos)
            else:
                print(f"  **  Box could not be moved: \n{boxes_ahead=}\n{empty_ahead=} ")
                return wharehouse

def w_print(wharehouse: Wharehouse) -> None:
    res = []
    for y in range(wharehouse.length):
        for x in range(wharehouse.width):
            if P(x, y) == wharehouse.robot_pos:
                print('@', end='')
            elif P(x, y) in wharehouse.boxes_pos:
                print('O', end='')
            elif P(x, y) in wharehouse.walls_pos:
                print('#', end='')
            else:
                print('.', end='')
        print(end='\n')
    print(end='\n')

def gps (wharehouse: Wharehouse) -> int:
    return sum([box.y *100 + box.x for box in wharehouse.boxes_pos])

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


test_wharehouse, test_moves = parse(RAW)
w_print(test_wharehouse)
for m in test_moves[:7]:
    print(f"=={m}\n{test_wharehouse.robot_pos=}")
    print(f"  {test_wharehouse.boxes_pos=}")
    test_wharehouse = move(m, test_wharehouse)
    w_print(test_wharehouse)
    print(f"  {test_wharehouse.robot_pos=}")
    print(f"  {test_wharehouse.boxes_pos=}")

"""
print("test : ", gps(test_wharehouse))
test_wharehouse_2, test_moves_2 = parse(RAW_2)
for m in test_moves_2:
    test_wharehouse_2 = move(m, test_wharehouse_2)
print("test 2 : ", gps(test_wharehouse_2))

test_wharehouse_2_final, test_moves_2_final = parse(RAW_2_final)
for m in test_moves_2_final:
    test_wharehouse_2_final = move(m, test_wharehouse_2_final)

print("test 2 final: ", gps(test_wharehouse_2_final))


print(f"==\n{test_wharehouse_2.width=}\n{test_wharehouse_2.length=}\n{test_wharehouse_2.robot_pos=}")
pprint(f"{test_wharehouse_2.boxes_pos=}\n==")


print(f"==\n{test_wharehouse_2_final.width=}\n{test_wharehouse_2_final.length=}\n{test_wharehouse_2_final.robot_pos=}")
pprint(f"{test_wharehouse_2_final.boxes_pos=}\n==")

pprint(f"{set(test_wharehouse_2.boxes_pos)=}\n==")
pprint(f"{set(test_wharehouse_2_final.boxes_pos) - set(test_wharehouse_2.boxes_pos) =}")

"""
"""
with open("day15.txt") as f:
    data = f.read()
wharehouse, moves = parse(data)
# print(wharehouse)
# print(moves)


"""
