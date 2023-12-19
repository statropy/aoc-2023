# day18.py 2023
import unittest
import logging
from typing import Literal

# from queue import Queue

logging.basicConfig(level=logging.INFO)


class Pos(object):
    NEXTPOS: dict = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
    TURNDICT = {
        "NE": "R",
        "NW": "L",
        "SE": "L",
        "SW": "R",
        "EN": "L",
        "ES": "R",
        "WN": "R",
        "WS": "L",
    }
    SIDEDICT = {
        "NR": (1, 0),
        "NL": (-1, 0),
        "SR": (-1, 0),
        "SL": (1, 0),
        "ER": (0, 1),
        "EL": (0, -1),
        "WR": (0, -1),
        "WL": (0, 1),
    }
    maxx: int = 0
    maxy: int = 0
    minx: int = 0
    miny: int = 0
    grid: set["Pos"] = set()
    side: Literal["L", "R"] | None = None
    steps: tuple[str, int, int]
    start: "Pos"
    nq: list["Pos"]

    @classmethod
    def trace(cls, lines: list[str], part: int = 1):
        if part == 1:
            cls.steps = [
                ("NSEW"["UDRL".index(d)], int(m), int(c[2:-1], 16))
                for d, m, c in [line.strip().split(" ") for line in lines]
            ]
        else:
            cls.steps = [
                ("ESWN"[c & 0xF], c >> 4, 0)
                for c in [int(line.strip().split(" ")[2][2:-1], 16) for line in lines]
            ]
        cls.nq = []
        cls.grid = set()
        cls.start = Pos()
        logging.debug(cls.start)
        turns = ""
        pos = cls.start
        for d, m, c in cls.steps:
            if pos.direction and pos.direction + d in cls.TURNDICT:
                turns += cls.TURNDICT[pos.direction + d]
            for _ in range(m):
                pos = pos.spawn(d, "path", c)
                logging.debug(pos)

        logging.debug(turns)
        if turns.count("L") > turns.count("R"):
            logging.debug("LEFT")
            cls.side = "L"
        else:
            logging.debug("RIGHT")
            cls.side = "R"

        cls.nq = [p for p in cls.grid if p.type == "path"]
        while len(cls.nq) > 0:
            pos = cls.nq.pop()
            logging.debug(f"A{pos} {pos.direction}")
            pos.add_neighbor()

        logging.debug(f"({cls.minx},{cls.miny}) ({cls.maxx},{cls.maxy})")
        logging.debug(cls.maxx * cls.maxy)
        return len(cls.grid)

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        before: "Pos" = None,
        direction: Literal["N", "S", "E", "W"] | None = None,
        type: Literal["path", "inner", "outer"] | None = None,
        color=0,
    ):
        self.x: int = x
        self.y: int = y
        self.last: Pos = before
        self.after: Pos = None
        self.direction: Literal[
            "N", "S", "E", "W"
        ] | None = direction  # the direction before went to get here
        self.type: Literal["path", "inner", "outer"] | None = type
        self.color: int = color
        Pos.minx = min(x, self.minx)
        Pos.miny = min(y, self.miny)
        Pos.maxx = max(x, self.maxx)
        Pos.maxy = max(y, self.maxy)

    def __repr__(self):
        return f"({self.x},{self.y} #{self.color:06x} {self.type})"

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other):
        return isinstance(other, Pos) and self.x == other.x and self.y == other.y

    def spawn(
        self,
        d: Literal["N", "S", "E", "W"],
        type: Literal["path", "inner", "outer"],
        color: int,
    ) -> "Pos":
        x, y = self.NEXTPOS[d]
        p = Pos(self.x + x, self.y + y, self, d, type, color)
        self.after = p
        self.grid.add(self)
        return p

    def add_neighbor(self):
        if self.type == "path":
            dx, dy = self.SIDEDICT[self.direction + self.side]
            n = Pos(self.x + dx, self.y + dy, self, None, "inner")
            if n not in self.grid:
                logging.debug(f"{n} {n.direction}")
                self.grid.add(n)
                self.nq.append(n)
                # n.add_neighbor()
        elif self.type == "inner":
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                n = Pos(self.x + dx, self.y + dy, self, type="inner")
                if n not in self.grid:
                    logging.debug(f"{n} {n.direction}")
                    self.grid.add(n)
                    self.nq.append(n)
                    # n.add_neighbor()
        else:
            logging.error(f"Unexpected type {self.type}")


def part1(lines: list[str]) -> int:
    return Pos.trace(lines)


def part2(lines: list[str]) -> int:
    return Pos.trace(lines, 2)


class TestDay18(unittest.TestCase):
    def test_1a(self):
        with open("./test18.txt", "r") as f:
            self.assertEqual(part1(list(f)), 62)

    def test_1(self):
        with open("./input18.txt", "r") as f:
            self.assertEqual(part1(list(f)), 49897)

    # def test_2a(self):
    #     with open("./test18.txt", "r") as f:
    #         self.assertEqual(part2(list(f)), 952408144115)

    # def test_2(self):
    #     with open('./input18.txt', 'r') as f:
    #         self.assertEqual(part2(list(f)), None)


if __name__ == "__main__":
    unittest.main()
