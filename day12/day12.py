from __future__ import annotations
from collections import defaultdict
from typing import NamedTuple, List, Tuple, Dict, Set, Optional


RAW = """AAAA
BBCD
BBCC
EEEC
AAAA
"""

RAW_2 = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""


class Point(NamedTuple):
    x: int
    y: int
    plant: str


class Garden:
    raw: str
    plants: defaultdict[List[Point]]

    def __init__(self, raw: str, plants=defaultdict(list)) -> None:
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
            return f"<Garden> with plants(num_points) : { { k: len(v) for k, v in self.plants.items() } } \n "
        return f"<Garden> with plants(num_points) : { { k: len(v) for k, v in self.plants.items() } } \n{self.plants=}\n"


class GardenPlots:
    garden: Garden
    regions: defaultdict[List[Set[Point]]]

    def __init__(self, garden: Garden, regions=defaultdict(list)) -> None:
        self.garden = garden
        self.regions = regions

    def __str__(self):
        regions_num_points = {k: len(v) for k, v in self.regions.items()}

        return f"<GardenPlots> with regions:num_points : { regions_num_points } \n{self.regions=}"

    def add_point_to_garden_plot(
        self, point: Point, new_point: Optional[Point]
    ) -> None:
        if len(self.regions[point.plant]) == 0:
            # if there is no region defined yet, define one and add points
            region = set()
            region.add(point)
            if new_point is not None:
                region.add(new_point)
            self.regions[point.plant].append(region)
            return
        else:
            # else check in the list of sets of regions for the region that the point belongs to and add the neighboor (new_point)
            for region in self.regions[point.plant]:
                if point in region and new_point is not None:
                    region.add(new_point)
                    break
                elif point in region and new_point is None:
                    # single point new region
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
        counter = 0
        if len(self.regions.values()) < 2:
            return self
        while True:
            # for each point of a region check if it's also in another region
            for plant, regions in self.regions.items():
                for r1, r2 in zip(regions, regions[1:]):
                    if bool(r1.intersection(r2)):
                        # if they intersect merge the two regions
                        r1.update(r2)
                        self.regions[plant].remove(r2)
                        counter += 1
                    counter += 1
                    if counter > 4:
                        break
                break
            break


def main():
    # with open("day12.txt") as f:
    #     raw = f.read()
    # garden = parse_input(RAW)
    # print(garden, garden.plants, sep="\n")

    # garden_plots = find_regions(garden)
    # print("\n", garden_plots, garden_plots.regions, sep="\n")

    garden_2 = Garden(RAW_2)
    print(garden_2)

    garden_plots_2 = GardenPlots(garden_2).find_regions()
    print(garden_plots_2)

    garden_plots_2.merge_regions()


if __name__ == "__main__":
    main()
