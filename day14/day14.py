from typing import NamedTuple
from dataclasses import dataclass

class P(NamedTuple):
    x: int
    y: int

class V(NamedTuple):
    x: int
    y: int

class Grid():

    def __init__(self, raw:str, tiles_wide: int, tiles_tall: int):
        self.tiles_wide = tiles_wide
        self.tiles_tall = tiles_tall
        self.points = []
        self.velocities = []
        self.parse(raw)
        self.grid = self.make_grid()


    def parse(self, raw: str):
        for line in raw.strip().split('\n'):
            p, v = line.split(' ')
            p = tuple([int(el) for el in p.strip('p=').split(',')])
            v = tuple([int(el) for el in v.strip('v=').split(',')])
            self.points.append(P(int(p[0]), int(p[1])))
            self.velocities.append(V(int(v[0]), int(v[1])))
        return

    def make_grid(self):
        grid = []
        for i in range(0, self.tiles_tall):
            row = []
            for j in range(0, self.tiles_wide):
                robots_at_location = [p for p in self.points if p == P(j, i)]
                if robots_at_location:
                    row.append(str(len(robots_at_location)))
                else:
                    row.append('.')
            grid.append(row)
        self.grid = grid

    def print_grid(self):
        for row in self.grid:
            print(''.join(row))

    def move(self):
        new_points = []
        for p, v in zip(self.points, self.velocities):
            mod_x = (p.x + v.x) % self.tiles_wide
            mod_y = (p.y + v.y) % self.tiles_tall
            new_p = P(mod_x, mod_y)
            new_points.append(new_p)
        self.points = new_points

    def no_duplicate(self):
        """assumption : when there are no two robots in one position, the christmas tree appears"""
        return not(len(set(self.points)) < len(self.points))

    def run(self):
        for _ in range(0, 100):
            self.move()
        self.make_grid()
        return self

    def run_2(self):
        for i in range(0, 10_000):
            self.move()
            if self.no_duplicate():
                break
        self.make_grid()
        return i + 1 # off by one error without adding 1, range starts at 0

    def safety_factor(self):
        q1 = [p for p in self.points if p.x <  self.tiles_wide // 2 and p.y < self.tiles_tall // 2]
        q2 = [p for p in self.points if p.x >  self.tiles_wide // 2 and p.y < self.tiles_tall // 2]
        q3 = [p for p in self.points if p.x >  self.tiles_wide // 2 and p.y > self.tiles_tall // 2]
        q4 = [p for p in self.points if p.x <  self.tiles_wide // 2 and p.y > self.tiles_tall // 2]
        return  len(q1) * len(q2) * len(q3) * len(q4)


RAW = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""

grid_test = Grid(RAW, 11, 7)
test_res = grid_test.run().safety_factor()
assert test_res == 12

with open('day14.txt') as f:
    raw = f.read()
grid = Grid(raw, 101, 103)
res = grid.run().safety_factor()
print(f"part 1: {res}")


res_2 = grid.run_2()
print(f"part 2: {res_2}")

