# day14.py 2023
import unittest
import numpy as np


def makecubes(lines: list[str]):  # -> np.array[np.array[int]]:
    return np.array(
        [
            [
                int(x, 2)
                for x in list(
                    line.strip().replace("O", "0").replace(".", "0").replace("#", "1")
                )
            ]
            for line in lines
        ]
    )


def makerocks(lines: list[str]) -> list[int]:
    return np.array(
        [
            [
                int(x, 2)
                for x in list(
                    line.strip().replace("O", "1").replace(".", "0").replace("#", "0")
                )
            ]
            for line in lines
        ]
    )


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


def tilt(rocks, cubes):
    # changed = True
    # lowest = len(cubes) - 1
    # for outer in range(len(cubes) - 1, -1, -1):
    # while lowest > 0:
    # while changed:
    # lowest = -1
    # r = 0
    for lowest in range(len(cubes) - 1, -1, -1):
        for i in range(lowest):
            rocks[i], rocks[i + 1] = (rocks[i] | rocks[i + 1]) & ~(cubes[i]), rocks[
                i + 1
            ] & ~(((cubes[i] | rocks[i]) ^ rocks[i + 1]) & rocks[i + 1])
            # # if not np.all(np.equal(a, rocks[i])):
            # if not changed and np.sum(a) != np.sum(rocks[i]):
            #     # if i > r:
            #     #     r = i
            #     changed = True
            # rocks[i] = a
        # lowest = r


def score(rocks: list[int]) -> int:
    return sum([(len(rocks) - y) * np.sum(rocks[y]) for y in range(len(rocks))])


def part1(lines: list[str]) -> int:
    cubes = makecubes(lines)
    rocks = makerocks(lines)
    tilt(rocks, cubes)
    return score(rocks)


def rotate(grid):
    return np.rot90(grid, axes=(1, 0))


def tupleize(a):
    return tuple(tuple(row) for row in a)


def part2(lines: list[str]) -> int:
    cubes = makecubes(lines)
    cubeslist = [cubes]
    for i in range(3):
        cubeslist.append(rotate(cubeslist[i]))

    rocks = makerocks(lines)
    cycles = 1000000000
    spin = 4
    order: dict[np.ndarray[np.ndarray[int]] : int] = {}
    rocklist = []
    for c in range(cycles):
        for orientation in range(spin):
            tilt(rocks, cubeslist[orientation])
            rocks = rotate(rocks)
        t = tupleize(rocks)
        if t in order:
            offset = order[t]
            loopsize = c - offset
            index = ((cycles - offset - 1) % loopsize) + offset
            return score(rocklist[index])
        else:
            order[t] = c
            rocklist.append(t)

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
