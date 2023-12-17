# day16.py 2023
import unittest
from typing import Literal


class Beam(object):
    grid: list[str]
    active: set["Beam"]
    WIDTH: int
    HEIGHT: int
    energized = dict[tuple[int, int] : [str]]

    @classmethod
    def Energize(
        cls,
        lines: list[str],
        x: int = -1,
        y: int = 0,
        d: Literal["N", "S", "E", "W"] = "E",
    ):
        cls.grid = lines
        cls.WIDTH = len(lines[0]) - 1
        cls.HEIGHT = len(lines)
        cls.active = set()
        cls.energized = {}
        cls.create(x, y, d)

        while len(cls.active) > 0:
            beams = [b for b in cls.active]
            for beam in beams:
                beam.step()

        return len(cls.energized)

    @classmethod
    def create(cls, x: int, y: int, d: Literal["N", "S", "E", "W"]):
        beam = Beam(x, y, d)
        cls.active.add(beam)

    def done(self):
        self.active.remove(self)

    def split(self, d: Literal["N", "S", "E", "W", "NS", "EW"]):
        for dd in d:
            self.create(self.px, self.py, dd)
        self.done()

    def __init__(self, x: int, y: int, d: Literal["N", "S", "E", "W"]):
        self.X = x
        self.Y = y
        self.D = d
        self.px = x
        self.py = y
        self.pd = d

    def __hash__(self) -> int:
        return hash((self.X, self.Y, self.D))

    def __eq__(self, other):
        return (
            isinstance(other, Beam)
            and self.X == other.X
            and self.Y == other.Y
            and self.D == other.D
        )

    def __repr__(self):
        return f"({self.px},{self.py}){self.pd}"

    def isvalid(self):
        return (
            self.px >= 0
            and self.px < self.WIDTH
            and self.py >= 0
            and self.py < self.HEIGHT
        )

    def charat(self):
        return self.grid[self.py][self.px]

    def index(self, d: Literal["N", "S", "E", "W"]):
        return 1 << "NSEW".index(d)

    def step(self):
        if self.pd == "E":
            self.px += 1
        elif self.pd == "W":
            self.px -= 1
        elif self.pd == "N":
            self.py -= 1
        else:  # "S"
            self.py += 1

        if not self.isvalid():
            self.done()
            return

        # if (self.px, self.py) in self.energized.keys():
        #     if self.pd in self.energized[(self.px, self.py)]:
        #         self.done()
        #         return
        #     else:
        #         self.energized[(self.px, self.py)] += self.pd
        # else:
        #     self.energized[(self.px, self.py)] = self.pd

        if (self.px, self.py) in self.energized:
            if self.index(self.pd) & self.energized[(self.px, self.py)] != 0:
                self.done()
                return
            else:
                self.energized[(self.px, self.py)] += self.index(self.pd)
        else:
            self.energized[(self.px, self.py)] = self.index(self.pd)

        at = self.charat()
        if at == "-" and self.pd in "NS":
            self.split("EW")
        elif at == "|" and self.pd in "EW":
            self.split("NS")
        elif at == "\\":
            self.split("WESN"["NSEW".index(self.pd)])
        elif at == "/":
            self.split("EWNS"["NSEW".index(self.pd)])


def part1(lines: list[str]) -> int:
    return Beam.Energize(lines)


def part2(lines: list[str]) -> int:
    Beam.Energize(lines)
    w = Beam.WIDTH
    h = Beam.HEIGHT
    entries = []
    for y in range(h):
        entries.append((-1, y, "E"))
        entries.append((w, y, "W"))
    for x in range(w):
        entries.append((x, -1, "S"))
        entries.append((x, h, "N"))

    return max([Beam.Energize(lines, x, y, d) for x, y, d in entries])


class TestDay16(unittest.TestCase):
    def test_1a(self):
        with open("./test16.txt", "r") as f:
            self.assertEqual(part1(list(f)), 46)

    def test_1(self):
        with open("./input16.txt", "r") as f:
            self.assertEqual(part1(list(f)), 6978)

    def test_2a(self):
        with open("./test16.txt", "r") as f:
            self.assertEqual(part2(list(f)), 51)

    def test_2(self):
        with open("./input16.txt", "r") as f:
            self.assertEqual(part2(list(f)), 7315)


if __name__ == "__main__":
    unittest.main()
