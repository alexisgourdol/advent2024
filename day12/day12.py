from __future__ import annotations
from typing import NamedTuple, List, Tuple, Dict, Set, Optional
from itertools import product
from pprint import pprint


class Point(NamedTuple):
    """Point class to represent a point <int, int> in a 2D grid"""

    x: int
    y: int

    def __str__(self):
        return f"P({self.x},{self.y})"

    def __repr__(self):
        return f"P({self.x},{self.y})"


class Garden:
    raw: str
    plants: Dict[List[Point]]

    def __init__(self, raw: str, plants=None) -> None:
        if plants is None:
            plants = {}
        self.plants = plants
        self.raw = raw

        for y, line in enumerate(self.raw.strip().split("\n")):
            for x, plant in enumerate(line):
                if not self.plants.get(plant):
                    self.plants[plant] = []
                self.plants[plant].append(Point(x, y))

    def __str__(self):
        shorten_output = (
            True
            if sum([len(points) for plant, points in self.plants.items()]) > 25
            else False
        )
        if shorten_output:
            return f"<Garden> with plants(num_points) : { { k: len(v) for k, v in self.plants.items() } }\n "
        else:
            pprint(dict(self.plants))
            return f"<Garden> with plants(num_points) : { { k: len(v) for k, v in self.plants.items() } }\n"


class GardenPlots:
    garden: Garden
    regions: Dict[List[Set[Point]]]

    def __init__(self, garden: Garden, regions=None) -> None:
        if regions is None:
            regions = {k: [] for k, v in garden.plants.items()}
        self.garden = garden
        self.regions = regions

    def __str__(self):
        regions_num_points = {k: len(v) for k, v in self.regions.items()}
        pprint(self.regions)
        # shorten_output = True if sum(regions_num_points.values()) > 25 else False
        # if shorten_output:
        # return f"<GardenPlots> with regions:num_points : { regions_num_points }\n"
        return f"<GardenPlots> with regions:num_points : { regions_num_points }\n"

    def find_regions(self) -> GardenPlots:
        """Loops over the garden points and adds each point to a region"""

        for y, line in enumerate(self.garden.raw.strip().split("\n")):
            for x, plant in enumerate(line):
                if len(self.regions[plant]) == 0:
                    region = set()
                    region.add(Point(x, y))
                    self.regions[plant].append(region)

                else:
                    for region in self.regions[plant]:
                        if plant == "I":
                            print(
                                f"HERE {plant=}, {self.regions[plant]=}, {Point(x,y)=}"
                            )
                        if (
                            Point(x - 1, y) in region
                            or Point(x, y - 1) in region
                            or Point(x + 1, y) in region
                            or Point(x, y + 1) in region
                        ):
                            region.add(Point(x, y))
                            break
                        else:
                            region = set()
                            print(f"adding  {Point(x,y)}")
                            region.add(Point(x, y))
                            self.regions[plant].append(region)
                        break
        return self

    def merge_regions(
        self,
    ) -> (
        GardenPlots
    ):  # wrong approach, need to check is_neighbour instead not intersections
        """Check for regions that are contiguous (that share a point)
        and merge them into a single region. Solves the case of a region embedded in another region
        """

        if len(self.regions.values()) < 2:
            return self
        # for each point of a region check if it's also in another region
        for plant, regions in self.regions.items():
            for r1, r2 in product(regions, regions[1:]):
                if bool(r1.intersection(r2)):
                    # if they intersect merge the two regions
                    r1.update(r2)
                    if r2 in self.regions[plant]:
                        self.regions[plant].remove(r2)
            break
        return self


if __name__ == "__main__":

    RAW_1 = """AAAA
BBCD
BBCC
EEEC
"""

    RAW_2 = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""

    RAW_3 = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

    # garden_1 = Garden(RAW_1)
    # print(RAW_1)
    # print(garden_1)
    # garden_plots_1 = GardenPlots(garden_1).find_regions()  # .merge_regions()
    # print(garden_plots_1)
    # print("=" * 80)

    # garden_2 = Garden(RAW_2)
    # print(RAW_2)
    # print(garden_2)
    # garden_plots_2 = GardenPlots(garden_2).find_regions()  # .merge_regions()
    # print(garden_plots_2)
    # print("=" * 80)

    # garden_3 = Garden(RAW_3)
    # print(RAW_3)
    # print(garden_3)
    # garden_plots_3 = GardenPlots(garden_3).find_regions()  # .merge_regions()
    # print(garden_plots_3)
    # print("=" * 80)

    # with open("day12.txt") as f:
    #     raw = f.read()
    #     garden = Garden(raw)
    #     print(garden)
    #     garden_plots = GardenPlots(garden).find_regions().merge_regions()
    #     print(garden_plots)

    class P(NamedTuple):
        x: int
        y: int

    d = {}
    for y, line in enumerate(RAW_3.strip().split("\n")):
        for x, plant in enumerate(line):
            if plant not in d:
                d[plant] = []

    d_set = {k: [] for k, v in d.items()}
    pprint(d_set)
    for y, line in enumerate(RAW_3.strip().split("\n")):
        for x, plant in enumerate(line):
            if len(d_set[plant]) == 0:
                print(f"new key {plant=} created")
                region = set()
                region.add(P(x, y))
                print(f"new region {region=} added")
                d_set[plant].append(region)
            else:
                for region in d_set[plant]:
                    if (
                        P(x - 1, y) in region
                        or P(x, y - 1) in region
                        or P(x + 1, y) in region
                        or P(x, y + 1) in region
                    ):
                        print(
                            f"{plant=}, neighbour found in existing region {region=}, adding  {P(x,y)=} added"
                        )
                        region.add(P(x, y))
                        break
                    else:
                        print(
                            f"{plant=}no neighbour found in existing regions, creating new region"
                        )
                        region = set()
                        print(f"adding  {P(x,y)=} added")
                        region.add(P(x, y))
                        d_set[plant].append(region)
                        break
