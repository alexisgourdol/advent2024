# https://gitlab.com/0xdf/aoc2024/-/blob/main/day09/day9.py?ref_type=heads

import sys


with open("day09.txt", "r") as f:
    data = list(map(int, f.read().strip()))

disk = []
for i in range(0, len(data), 2):
    disk.extend(data[i] * [i // 2])
    if i + 1 < len(data):
        disk.extend(data[i + 1] * [-1])
print(f"{disk[:30]=}")

empties = [i for i, val in enumerate(disk) if val == -1]
print(f"{empties[:30]=}")

i = 0
while True:
    if i > 5: break
    # remove trailing -1s
    while disk[-1] == -1:
        disk.pop()
    target = empties[i]
    print(f"{target=}")
    # when last empty target is beyond the length of the disk, we're sure to be done
    if target >= len(disk):
        break
    disk[target] = disk.pop()
    i += 1

part1 = sum(i * val for i, val in enumerate(disk))
print(f"Part 1: {part1}")
