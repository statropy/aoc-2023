# day10.py 2023
import unittest
import logging
from typing import Literal


class Pos(object):
    nextpos: dict = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}

    def __init__(self, grid: "Grid", x: int, y: int, last: "Pos" = None):
        if x < 0 or y < 0 or x >= grid.width or y >= grid.height:
            raise ValueError("Invalid index")
        self.x: int = x
        self.y: int = y
        self.grid: Grid = grid
        if last is not None and self == last:
            raise ValueError("Backtracking")
        self.last = last

    def __repr__(self):
        return f"({self.x},{self.y})"

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other):
        return isinstance(other, Pos) and self.x == other.x and self.y == other.y

    def _move(self, x: int, y: int) -> "Pos":
        return Pos(self.grid, self.x + x, self.y + y, self)

    def move(self, direction: Literal["N", "S", "E", "W"]):
        try:
            p = self._move(*self.nextpos[direction])
            # logging.debug(f"{self} -> {p}")
            self.grid.add(p, direction)
            # if (
            #     self.grid.tile(p) in self.legal[direction]
            #     and p not in self.grid.visited
            # ):
            #     self.grid.add(p)
        except ValueError:
            pass  # invalid
        # except Exception as e:
        #     print(e, type(e), self, self.last)

    # def coords(self):
    #     return (self.x, self.y)


class Grid(object):
    legal = {"N": "|7F", "S": "|LJ", "E": "-J7", "W": "-LF"}
    # legal = {
    #     "N": [ord("|"), ord("7"), ord("F")],
    #     "S": [ord("|"), ord("L"), ord("J")],
    #     "E": [ord("-"), ord("J"), ord("7")],
    #     "W": [ord("-"), ord("L"), ord("F")],
    # }

    def __init__(self, lines: list[str]):
        # self.grid = lines
        self.grid = []
        self.start: Pos = None
        self.nextstep = []
        self.steps = 0
        self.answer = 0
        self.left = None
        self.right = None

        for y, row in enumerate(lines):
            self.grid.append([c for c in row.strip()])
            if self.start is None:
                try:
                    x = row.index("S")
                    start = Pos(self, x, y)
                    self.current = set([start])
                    self.visited = set([start])
                    # self.grid[-1][x] = 0
                except ValueError:
                    continue

    def tile(self, pos: Pos) -> str:
        return self.grid[pos.y][pos.x]

    @property
    def width(self) -> int:
        return len(self.grid[0])

    @property
    def height(self) -> int:
        return len(self.grid)

    def add(self, pos: Pos, direction: Literal["N", "S", "E", "W"]):
        if self.tile(pos) in self.legal[direction]:
            logging.debug(f" {direction} {pos.last} -> {pos} {self.tile(pos)}")
            self.nextstep.append(pos)

    def findloop(self):
        while len(self.current) > 0:
            if logging.getLogger().level == logging.DEBUG:
                print("-" * 50)
            self.nextstep = []
            # for pos in self.current:
            #     self.grid[pos.y][pos.x] = " "
            for pos in self.current:
                for d in "NSEW":
                    pos.move(d)
            self.current = set(self.nextstep)

            self.steps += 1

            for pos in self.current:
                self.grid[pos.y][pos.x] = "*"  # ord("*")
            # if len(self.nextstep) == 2 and self.nextstep[0] == self.nextstep[1]:
            if len(self.current) != len(self.nextstep):
                if self.left is not None:
                    self.grid[self.left.y][self.right.x] = " "
                found = set()
                for pos in self.nextstep:
                    if pos in found:
                        self.left = pos
                        logging.debug(f"Remove {pos}")
                        self.current.remove(pos)
                    else:
                        found.add(pos)
                for pos in self.nextstep:
                    if pos == self.left:
                        self.right = pos
                        self.grid[pos.y][pos.x] = "+"
                logging.debug(f"A: {self.steps} {self.current} {self.nextstep}")
                self.answer = self.steps
            if logging.getLogger().level == logging.DEBUG:
                print(self)
            for pos in self.current:
                self.grid[pos.y][pos.x] = " "
        for pos in self.current:
            self.grid[pos.y][pos.x] = " "
        print(self.current)
        return self.answer

    def retrace(self):
        pass

    def __repr__(self):
        output = ""
        for row in self.grid:
            output += ("".join([c for c in row])) + "\n"
        return output


def part1(lines: list[str]) -> int:
    grid = Grid(lines)
    a = grid.findloop()
    print(grid)
    return a


def part2(lines: list[str]) -> int:
    grid = Grid(lines)
    grid.findloop()
    grid.retrace()
    # print(grid)

    return None


logging.basicConfig(level=logging.DEBUG)


class TestDay10(unittest.TestCase):
    # def test_1a(self):
    #     with open("./test10.txt", "r") as f:
    #         self.assertEqual(part1(list(f)), 4)

    # def test_1b(self):
    #     with open("./test10b.txt", "r") as f:
    #         self.assertEqual(part1(list(f)), 8)

    # def test_1(self):
    #     with open("./input10.txt", "r") as f:
    #         self.assertEqual(part1(list(f)), 6733)

    def test_2a(self):
        with open("./test10.txt", "r") as f:
            self.assertEqual(part2(list(f)), None)

    # def test_2(self):
    #     with open('./input10.txt', 'r') as f:
    #         self.assertEqual(part2(list(f)), None)


if __name__ == "__main__":
    unittest.main()
