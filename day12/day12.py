from __future__ import annotations
from collections import defaultdict
from typing import NamedTuple, List, Tuple, Dict, Set, Optional
from itertools import product
from pprint import pprint


class Point(NamedTuple):
    """Point class to represent a point <int, int> with a plant type <str>"""

    x: int
    y: int
    plant: str

    def __str__(self):
        return f"P({self.x},{self.y},{self.plant})"

    def __repr__(self):
        return f"P({self.x},{self.y},{self.plant})"


class Garden:
    raw: str
    plants: defaultdict[List[Point]]

    def __init__(self, raw: str, plants=None) -> None:
        if plants is None:
            plants = defaultdict(list)
        self.plants = plants
        self.raw = raw

        for y, line in enumerate(self.raw.strip().split("\n")):
            for x, plant in enumerate(line):
                self.plants[plant].append(Point(x, y, plant))

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
    regions: defaultdict[List[Set[Point]]]

    def __init__(self, garden: Garden, regions=None) -> None:
        if regions is None:
            regions = defaultdict(list)
        self.garden = garden
        self.regions = regions

    def __str__(self):
        regions_num_points = {k: len(v) for k, v in self.regions.items()}
        pprint(self.regions)
        # shorten_output = True if sum(regions_num_points.values()) > 25 else False
        # if shorten_output:
        # return f"<GardenPlots> with regions:num_points : { regions_num_points }\n"
        return f"<GardenPlots> with regions:num_points : { regions_num_points }\n"

    def add_point_to_garden_plot(
        self, point: Point, new_point: Optional[Point]
    ) -> None:
        """Assigns a Point (and its neigbour with the same plant type if any)
        to an existing region or creates a new region before assignment"""

        if len(self.regions[point.plant]) == 0:
            # if there is no region defined yet, define one and add points
            region = set()
            region.add(point)
            if new_point is not None:
                region.add(new_point)
            self.regions[point.plant].append(region)
            return
        else:
            # else check in the list of sets of regions for the region
            # that the point belongs to and add the neighboor (new_point)
            for region in self.regions[point.plant]:
                if point in region and new_point is not None:
                    region.add(new_point)
                    break
                elif point in region and new_point is None:
                    # single point new region; clunckuy but avoids potential creation of
                    # new region for last bottom right point ;
                    # should be no issue for merge point methodanyways
                    region.add(point)
                    break
                else:
                    # if there is no region for the point, create a new region
                    region = set()
                    region.add(point)
                    if new_point is not None:
                        region.add(new_point)
                    self.regions[point.plant].append(region)
                    break

    def find_regions(self) -> GardenPlots:
        """Loops over the garden points and adds each point to a region"""

        for plant, points in self.garden.plants.items():
            # {'A': [Point(x=0, y=0, plant='A'), Point(x=1, y=0, plant='A')], 'B' ...}
            for point in points:
                x, y = point.x, point.y
                if Point(x + 1, y, plant) in points:
                    self.add_point_to_garden_plot(point, Point(x + 1, y, plant))
                elif Point(x, y + 1, plant) in points:
                    self.add_point_to_garden_plot(point, Point(x, y + 1, plant))
                else:
                    self.add_point_to_garden_plot(point, new_point=None)

        return self

    def merge_regions(self) -> GardenPlots:
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

    garden_1 = Garden(RAW_1)
    print(RAW_1)
    print(garden_1)
    garden_plots_1 = GardenPlots(garden_1).find_regions()  # .merge_regions()
    print(garden_plots_1)
    print("=" * 80)

    garden_2 = Garden(RAW_2)
    print(RAW_2)
    print(garden_2)
    garden_plots_2 = GardenPlots(garden_2).find_regions().merge_regions()
    print(garden_plots_2)
    print("=" * 80)

    garden_3 = Garden(RAW_3)
    print(RAW_3)
    print(garden_3)
    garden_plots_3 = GardenPlots(garden_3).find_regions()  # .merge_regions()
    print(garden_plots_3)
    print("=" * 80)

    # with open("day12.txt") as f:
    #     raw = f.read()
    #     garden = Garden(raw)
    #     print(garden)
    #     garden_plots = GardenPlots(garden).find_regions().merge_regions()
    #     print(garden_plots)
