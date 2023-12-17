# day16.py 2023
import unittest
from typing import Literal


class Beam(object):
    grid: list[str]
    energized: list[bool]
    active: set["Beam"]
    finished: set["Beam"]
    WIDTH: int
    HEIGHT: int

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
        cls.energized = [False] * (cls.HEIGHT * cls.WIDTH)
        cls.active = set()
        cls.finished = set()
        cls.create(x, y, d)

        while len(cls.active) > 0:
            beams = [b for b in cls.active]
            for beam in beams:
                beam.step()
        # cls.show()

        return len([e for e in cls.energized if e])

    def isunique(self):
        return self not in self.active and self not in self.finished

    @classmethod
    def show(cls):
        print()
        for y in range(cls.HEIGHT):
            line = ""
            for x in range(cls.WIDTH):
                if cls.energized[y * cls.WIDTH + x]:
                    line += "#"
                else:
                    line += "."
            print(line)

    @classmethod
    def create(cls, x: int, y: int, d: Literal["N", "S", "E", "W"]):
        beam = Beam(x, y, d)
        if beam.isunique():
            cls.active.add(beam)

    def done(self):
        self.active.remove(self)
        self.finished.add(self)

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

        self.energized[self.py * self.WIDTH + self.px] = True

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
