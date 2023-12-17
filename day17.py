# day17.py 2023
import unittest
from typing import Literal
from queue import Queue


class Node(object):
    GRID: list[int]
    WIDTH: int
    HEIGHT: int
    part: int

    @classmethod
    def search(cls, lines: list[str], x: int = 0, y: int = 0, part: int = 1):
        cls.part = part
        cls.WIDTH = len(lines[0]) - 1
        cls.HEIGHT = len(lines)
        cls.GRID = [0] * (cls.HEIGHT * cls.WIDTH)
        for row in range(cls.HEIGHT):
            for col in range(cls.WIDTH):
                cls.GRID[row * cls.WIDTH + col] = int(lines[row][col])
        visited: dict["Node":int] = {}
        found: set[int] = set()
        q: Queue = Queue()
        start = Node(x, y, "")
        q.put(start)

        while not q.empty():
            n = q.get()
            for d in "NSEW":
                if n.backtrack(d):
                    continue
                child: Node = n.spawn(d)
                if child is None:
                    continue
                w = visited.get(child)
                chscore = child.score() + visited.get(n, 0)
                if w is None or chscore < w:
                    visited[child] = chscore
                    q.put(child)

                if child.atgoal():
                    found.add(visited[child])
        return min(found)

    def __init__(self, x: int, y: int, moving: str):
        self.x = x
        self.y = y
        self.d = moving

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.d))

    def __eq__(self, other):
        return (
            isinstance(other, Node)
            and self.x == other.x
            and self.y == other.y
            and self.d == other.d
        )

    def __repr__(self):
        return f"({self.x},{self.y}):{self.score(self)} [{self.d}]"

    def backtrack(self, d: Literal["N", "S", "E", "W"]):
        if self.d == "":
            return False
        return "SNWE"["NSEW".index(self.d[-1])] == d

    def isvalid(self, x: int, y: int, d: Literal["N", "S", "E", "W"]):
        if self.part == 1:
            return (
                x >= 0
                and x < self.WIDTH
                and y >= 0
                and y < self.HEIGHT
                and self.d + d != d * 4
            )
        a = (
            x >= 0
            and x < self.WIDTH
            and y >= 0
            and y < self.HEIGHT
            and self.d + d != d * 11
        )
        if a:
            if len(self.d) > 0 and len(self.d) < 4:
                return self.d == d * len(self.d)
        return a

    def atgoal(self) -> bool:
        return self.x == self.WIDTH - 1 and self.y == self.HEIGHT - 1

    def score(self) -> int:
        return self.GRID[self.y * self.WIDTH + self.x]

    def move(self, d: Literal["N", "S", "E", "W"]) -> tuple[int, int]:
        if d == "N":
            return (self.x, self.y - 1)
        if d == "S":
            return (self.x, self.y + 1)
        if d == "E":
            return (self.x + 1, self.y)
        return (self.x - 1, self.y)

    def spawn(self, d: Literal["N", "S", "E", "W"]):
        x, y = self.move(d)
        if self.isvalid(x, y, d):
            if d in self.d:
                d = self.d + d
            return Node(x, y, d)
        return None


def part1(lines: list[str]) -> int:
    return Node.search(lines)


def part2(lines: list[str]) -> int:
    return Node.search(lines, part=2)


class TestDay17(unittest.TestCase):
    def test_1a(self):
        with open("./test17.txt", "r") as f:
            self.assertEqual(part1(list(f)), 102)

    def test_1(self):
        with open("./input17.txt", "r") as f:
            self.assertEqual(part1(list(f)), 1260)

    def test_2a(self):
        with open("./test17.txt", "r") as f:
            self.assertEqual(part2(list(f)), 94)

    def test_2(self):
        with open("./input17.txt", "r") as f:
            self.assertEqual(part2(list(f)), 1416)


if __name__ == "__main__":
    unittest.main()
