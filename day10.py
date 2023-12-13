# day10.py 2023
import unittest
import logging
from typing import Literal


class Pos(object):
    nextpos: dict = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}

    def __init__(
        self,
        grid: "Grid",
        x: int,
        y: int,
        last: "Pos" = None,
        direction: Literal["N", "S", "E", "W"] = None,
    ):
        if x < 0 or y < 0 or x >= grid.width or y >= grid.height:
            raise ValueError("Invalid index")
        self.x: int = x
        self.y: int = y
        self.grid: Grid = grid
        self.last = last
        self.direction = direction  # the direction last went to get here

    def __repr__(self):
        return f"({self.x},{self.y})"

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other):
        return isinstance(other, Pos) and self.x == other.x and self.y == other.y

    def spawn(self, x: int, y: int, direction: Literal["N", "S", "E", "W"]) -> "Pos":
        return Pos(self.grid, self.x + x, self.y + y, self, direction)

    def move(self, direction: Literal["N", "S", "E", "W"]):
        try:
            p = self.spawn(*self.nextpos[direction], direction)
            if self.last is None or self.last != p:
                self.grid.add(p, direction)
        except ValueError as e:
            logging.debug(e)


class Grid(object):
    legal_to = {"N": "|7F", "S": "|LJ", "E": "-J7", "W": "-LF"}
    legal_from = {"N": "S|LJ", "S": "S|7F", "E": "S-LF", "W": "S-J7"}

    def __init__(self, lines: list[str]):
        self.grid = []
        self.display = []
        self.start: Pos = None
        self.nextstep = []
        self.steps = 0
        self.pinner = set()
        self.pending = set()
        self.inc = None
        self.outc = None

        for y, row in enumerate(lines):
            self.grid.append([c for c in row.strip()])
            self.display.append([c for c in row.strip()])
            if self.start is None:
                try:
                    x = row.index("S")
                    self.start = Pos(self, x, y)
                    self.current = set([self.start])
                    self.visited = set([self.start])
                except ValueError:
                    continue

    def gridtile(self, pos: Pos) -> str:
        return self.grid[pos.y][pos.x]

    def gridtileat(self, x: int, y: int) -> str:
        return self.grid[y][x]

    def tile(self, pos: Pos) -> str:
        return self.display[pos.y][pos.x]

    def tileat(self, x: int, y: int) -> str:
        return self.display[y][x]

    def clearat(self, x: int, y: int):
        self.display[y][x] = " "

    def mark(self, pos: Pos, c: str = " "):
        self.display[pos.y][pos.x] = c

    def markcurrent(self, pos: Pos):
        self.mark(pos, "*")

    def markouterat(self, x: int, y: int):
        p = Pos(self, x, y)
        self.markouter(p)

    def markouter(self, pos: Pos):
        self.mark(pos, "O")

    def markinner(self, pos: Pos):
        self.mark(pos, "I")
        self.pinner.add(pos)

    def markinnerat(self, x: int, y: int):
        p = Pos(self, x, y)
        self.markinner(p)

    def markpath(self, pos: Pos):
        self.mark(pos, "+")

    def markright(self, pos: Pos):
        self.mark(pos, "R")

    def markleft(self, pos: Pos):
        self.mark(pos, "Q")

    @property
    def width(self) -> int:
        return len(self.grid[0])

    @property
    def height(self) -> int:
        return len(self.grid)

    def add(self, pos: Pos, direction: Literal["N", "S", "E", "W"]):
        if (
            self.gridtile(pos) in self.legal_to[direction]
            and self.gridtile(pos.last) in self.legal_from[direction]
        ):
            logging.debug(f" {direction} {pos.last} -> {pos} {self.gridtile(pos)}")
            self.nextstep.append(pos)

    def findloop(self):
        while len(self.current) > 0:
            if logging.getLogger().level == logging.DEBUG:
                print("-" * 50)
            self.nextstep = []
            for pos in self.current:
                for d in "NSEW":
                    pos.move(d)
            self.current = set(self.nextstep)

            self.steps += 1

            for pos in self.current:
                self.markcurrent(pos)
            if len(self.current) == 1 and len(self.nextstep) == 2:
                logging.debug(f"A: {self.steps} {self.current} {self.nextstep}")
                self.current = set()
                self.markpath(self.nextstep[0])
            if logging.getLogger().level == logging.DEBUG:
                print(self)
            for pos in self.current:
                self.mark(pos)
        for pos in self.current:
            self.mark(pos)
        return self.steps

    def markside(self, pos: Pos, x, y, d, f, o):
        try:
            n = pos.spawn(x, y, d)
            if self.tile(n) != "+":
                if (d == f) != (o == "flip"):
                    self.markright(n)
                else:
                    self.markleft(n)
        except ValueError as e:
            logging.debug(e)

    def side(
        self,
        pos: Pos,
        direction: Literal["N", "S", "E", "W"],
        tile: Literal["|", "-", "L", "J", "7", "F"],
        orientation: Literal["norm", "flip"],
    ):
        if tile == "|":
            self.markside(pos, 1, 0, direction, "N", orientation)
            self.markside(pos, -1, 0, direction, "S", orientation)
        elif tile == "-":
            self.markside(pos, 0, 1, direction, "E", orientation)
            self.markside(pos, 0, -1, direction, "W", orientation)
        elif tile == "J":
            self.markside(pos, 1, 0, direction, "N", orientation)
            self.markside(pos, 0, 1, direction, "N", orientation)
            self.markside(pos, -1, -1, direction, "W", orientation)
            pass
        elif tile == "F":
            self.markside(pos, 0, -1, direction, "S", orientation)
            self.markside(pos, -1, 0, direction, "S", orientation)
            self.markside(pos, 1, 1, direction, "E", orientation)
            pass
        elif tile == "L":
            self.markside(pos, 1, -1, direction, "N", orientation)
            self.markside(pos, 0, 1, direction, "E", orientation)
            self.markside(pos, -1, 0, direction, "E", orientation)
            pass
        elif tile == "7":
            self.markside(pos, -1, 1, direction, "S", orientation)
            self.markside(pos, 0, -1, direction, "W", orientation)
            self.markside(pos, 1, 0, direction, "W", orientation)
            pass

    def retrace_path(self, node, orientation):
        while node.last is not None:
            self.markpath(node)
            self.side(node.last, node.direction, self.gridtile(node.last), orientation)
            node = node.last

    def count(self, c):
        return len([c for row in self.display for col in row if col == c])

    def other(self, c):
        if c == "R":
            return "Q"
        return "R"

    def retrace(self):
        a: Pos
        b: Pos
        a, b = self.nextstep
        self.markpath(self.start)
        self.retrace_path(a, "norm")
        self.retrace_path(b, "flip")

        for y, row in enumerate(self.display):
            for x, col in enumerate(row):
                if col not in "+QR":
                    self.clearat(x, y)

        for y, row in enumerate(self.display):
            for x, col in enumerate(row):
                tile = self.tileat(x, y)
                if tile == "+":
                    continue
                p = Pos(self, x, y)
                if self.inc is not None and tile in "RQ":
                    if tile == self.inc:
                        self.markinner(p)
                    else:
                        self.markouter(p)
                elif tile in " RQ":
                    me = self.checkNeighbors(p)
                    if self.inc is None and tile in "RQ":
                        if me == "O":
                            self.outc = tile
                            self.inc = self.other(tile)
                        else:
                            self.inc = tile
                            self.outc = self.other(tile)
                        logging.debug(f"FOUND  {me} I={self.inc} O={self.outc}")
                    if me == "O":
                        self.markouter(p)
                    elif me == "I":
                        self.markinner(p)
        return len(self.pinner)

    def checkNeighbors(self, pos: Pos):
        dirs = ["W", "N", "E", "S"]
        for i, (x, y) in enumerate([(-1, 0), (0, -1), (1, 0), (0, 1)]):
            try:
                n = pos.spawn(x, y, dirs[i])
                t = self.tile(n)
                tile = self.tile(pos)

                if n in self.pending:
                    continue

                if t in "OIRQ":
                    return t
                if t == " ":
                    if tile == "O":
                        self.markouter(n)
                        continue
                    elif tile == "I":
                        self.markinner(n)
                        continue
                    self.pending.add(pos)
                    t = self.checkNeighbors(n)
                    self.pending.remove(pos)
                    return t
            except ValueError:
                return "O"

        raise AssertionError

    def __repr__(self):
        output = ""
        for row in self.display:
            output += ("".join([c for c in row])) + "\n"
        return output

    def show(self):
        output = ""
        for row in self.grid:
            output += ("".join([c for c in row])) + "\n"
        return output


def part1(lines: list[str]) -> int:
    grid = Grid(lines)
    return grid.findloop()


def part2(lines: list[str]) -> int:
    grid = Grid(lines)
    grid.findloop()
    return grid.retrace()


logging.basicConfig(level=logging.INFO)


class TestDay10(unittest.TestCase):
    def test_1a(self):
        with open("./test10.txt", "r") as f:
            self.assertEqual(part1(list(f)), 4)

    def test_1b(self):
        with open("./test10b.txt", "r") as f:
            self.assertEqual(part1(list(f)), 8)

    def test_1(self):
        with open("./input10.txt", "r") as f:
            self.assertEqual(part1(list(f)), 6733)

    def test_2c(self):
        with open("./test10c.txt", "r") as f:
            self.assertEqual(part2(list(f)), 4)

    def test_2d(self):
        with open("./test10d.txt", "r") as f:
            self.assertEqual(part2(list(f)), 8)

    def test_2e(self):
        with open("./test10e.txt", "r") as f:
            self.assertEqual(part2(list(f)), 10)

    def test_2(self):
        with open("./input10.txt", "r") as f:
            self.assertEqual(part2(list(f)), 435)


if __name__ == "__main__":
    unittest.main()
