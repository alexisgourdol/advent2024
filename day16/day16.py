from queue import Queue
from typing import List, NamedTuple

class P(NamedTuple):
    x: int
    y: int


def solve(maze):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    walls : List[P] = []
    start : P = None
    end : P = None
    rows = len(maze)
    cols = len(maze[0])
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == ".":
                continue
            elif maze[i][j] == "#":
                walls.append(P(i, j))
            elif maze[i][j] == "S":
                start = P(i, j)
            elif maze[i][j] == "E":
                end = P(i, j)
            else:
                raise ValueError(f"Invalid character in maze at {(i,j)=}")
    print(f"{start=}, {end=}")

    visited = [start]
    queue = Queue()
    queue.put((start, []))

    while not queue.empty():
        (node, path) = queue.get()
        for dx, dy in directions:
            next_node = P(node.x+dx, node.y+dy)

            if (next_node == end):
                final_path = path + [next_node]
                num_turns = detect_turns(path)
                if P(start.x, start.y + 1) not in final_path:
                    # TO DO check other init corner case e.g. need to turn twice to start the maze
                    num_turns += 1 # Start face east, so if first step is not east, we starting by turning
                return final_path, num_turns

            if (0 <= next_node.x  < rows and
                0 <= next_node.y  < cols and
                next_node not in walls + visited):
                visited.append(next_node)
                queue.put((next_node, path + [next_node]))


def maze_print(maze, path):
    rows = len(maze)
    cols = len(maze[0])
    print("  ", "".join([str(i).rjust(3) for i in range(cols)]))
    for i in range(rows):
        print(str(i).rjust(2), end=" ")
        for j in range(cols):
            if maze[i][j] == "E":
                print("E".rjust(3), end="")
            elif (i, j) in path:
                print("X".rjust(3), end="")
            elif maze[i][j] == "#":
                print("#".rjust(3), end="")
            elif maze[i][j] == "S":
                print("S".rjust(3), end="")
            else:
                print(".".rjust(3), end="")
        print()

def detect_turns(path):
    turns_at = [] # might need this later to add a constraint # right after the turn and compute new calc
    counter = 0
    for i in range(1, len(path)-2):
        prev_node = path[i-1]
        node = path[i]
        next_node = path[i+1]
        turns_at.append((prev_node, node, next_node))
        if prev_node.x == node.x == next_node.x:
            continue
        if prev_node.y == node.y == next_node.y:
            continue
        counter += 1
    return counter

def score(path, num_turns):
    return len(path) + 1000 * num_turns

def simulate_multiple_paths(maze):
    # think of recursive solution
    # or detect where the turns occur and place a wall #
        # then solve the maze and compute the score
        # rank path by lowest scores
        # idea : at some point, the turns will be a dead end, focing the path to be longer but with lower costly turns
        # check if placing wall doest't trap the user
    ...


if __name__ == "__main__":
    ex1 = "ex1.txt"
    ex2 = "ex2.txt"
    ex1_solved = "ex1_solved.txt"
    ex2_solved = "ex2_solved.txt"
    inp = "day16.txt"

    selected_input = inp #<-- change here

    with open(selected_input) as f:
        maze = f.read().splitlines()

    final_path, num_turns = solve(maze)
    print(f"{selected_input}: {score(final_path, num_turns)}")


    if selected_input == ex1:
        assert score(final_path, num_turns) == 7036
    elif selected_input == ex2:
        assert score(final_path, num_turns) == 11048
    elif selected_input == inp:
        assert score(final_path, num_turns) < 79392 # value is too high
