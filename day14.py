# day14.py 2023
import unittest
import numpy as np


def makecubes(lines: list[str]) -> list[int]:
    return [
        int(line.strip().replace("O", "0").replace(".", "0").replace("#", "1"), 2)
        for line in lines
    ]


def makerocks(lines: list[str]) -> list[int]:
    return [
        int(line.strip().replace("O", "1").replace(".", "0").replace("#", "0"), 2)
        for line in lines
    ]


def show(rocks, cubes, width):
    print()
    for y in range(len(rocks)):
        for x in range(width - 1, -1, -1):
            if cubes[y] & (1 << x) != 0 and rocks[y] & (1 << x) != 0:
                print("!", end="")
            elif cubes[y] & (1 << x) != 0:
                print("#", end="")
            elif rocks[y] & (1 << x) != 0:
                print("O", end="")
            else:
                print(".", end="")
        print(f" {len(rocks)-y:2}")


def tilt(rocks, cubes, cols=0):
    changed = True
    while changed:
        if cols:
            show(rocks, cubes, cols)
        changed = False
        for i in range(len(cubes) - 1):
            a = (rocks[i] | rocks[i + 1]) & ~(cubes[i])
            rocks[i + 1] = rocks[i + 1] & ~(
                ((cubes[i] | rocks[i]) ^ rocks[i + 1]) & rocks[i + 1]
            )
            if a != rocks[i]:
                changed = True
            rocks[i] = a


def score(rocks: list[int]) -> int:
    return sum([(len(rocks) - y) * rocks[y].bit_count() for y in range(len(rocks))])


def part1(lines: list[str]) -> int:
    cubes = makecubes(lines)
    rocks = makerocks(lines)
    cols = 0
    tilt(rocks, cubes, cols)
    return score(rocks)


def rotate(grid: list[int], width):
    m = np.array([list(f"{x:0{width}b}") for x in grid])
    mr = np.rot90(m, axes=(1, 0))
    return [int("".join(row), 2) for row in mr]


def part2(lines: list[str]) -> int:
    widths = [len(lines[0].strip()), len(lines)]
    cubes = makecubes(lines)
    cubeslist = [cubes]
    for i in range(3):
        cubeslist.append(rotate(cubeslist[i], widths[i % 2]))

    rocks = makerocks(lines)
    cycles = 1000000000
    spin = 4
    order = {}
    rocklist = []
    for c in range(cycles):
        for orientation in range(spin):
            tilt(rocks, cubeslist[orientation])
            rocks = rotate(rocks, widths[orientation % 2])
        if tuple(rocks) in order:
            offset = order[tuple(rocks)]
            loopsize = c - offset
            index = ((cycles - offset - 1) % loopsize) + offset
            return score(rocklist[index])
        else:
            order[tuple(rocks)] = c
            rocklist.append(tuple(rocks))

    return score(rocks)


class TestDay14(unittest.TestCase):
    def test_1a(self):
        with open("./test14.txt", "r") as f:
            self.assertEqual(part1(list(f)), 136)

    def test_1(self):
        with open("./input14.txt", "r") as f:
            self.assertEqual(part1(list(f)), 108614)

    def test_2a(self):
        with open("./test14.txt", "r") as f:
            self.assertEqual(part2(list(f)), 64)

    def test_2(self):
        with open("./input14.txt", "r") as f:
            self.assertEqual(part2(list(f)), 96447)


if __name__ == "__main__":
    unittest.main()
