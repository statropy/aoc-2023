# day17.py 2023
import unittest
from typing import Literal
from queue import Queue


class Node(object):
    GRID: list[int]
    WIDTH: int
    HEIGHT: int
    visited: dict["Node":int]
    q: Queue
    found: set[int]

    @classmethod
    def search(cls, lines: list[str], x: int = 0, y: int = 0):
        cls.WIDTH = len(lines[0]) - 1
        cls.HEIGHT = len(lines)
        cls.GRID = [0] * (cls.HEIGHT * cls.WIDTH)
        for row in range(cls.HEIGHT):
            for col in range(cls.WIDTH):
                cls.GRID[row * cls.WIDTH + col] = int(lines[row][col])
        cls.visited = {}
        cls.found = set()
        cls.q = Queue()
        start = Node(x, y, "")
        cls.q.put(start)
        # cls.visited[start] = 0
        count = 0

        while not cls.q.empty():
            p = False
            count += 1
            n = cls.q.get()
            # print(count)
            # if n.x == 8 and n.y == 2:
            #     print("Hello!", n)
            #     p = True
            for d in "NSEW":
                if n.backtrack(d):
                    if p:
                        print("backtrack", d)
                    continue
                child: Node = n.spawn(d)
                if child is None:
                    continue
                # if child in cls.visited:
                w = cls.visited.get(child)
                chscore = cls.score(child.x, child.y) + cls.visited.get(n, 0)
                if w is None or chscore < w:
                    cls.visited[child] = chscore
                    cls.q.put(child)

                if child.atgoal():
                    if p:
                        print("Found from", n, "=>", child)
                    cls.found.add(cls.visited[child])
                #     # if len(cls.found) > 0 and child.weight >= min(cls.found):
                #     #     if p:
                #     #         print("Bail  from", n, "=>", child)
                #     # else:
                #         if p:
                #             print("Add   from", n, "=>", child)
                #         cls.q.put(child)
                # else:
                #     if p:
                #         print("Repeat", child)

        return min(cls.found)

    def __init__(self, x: int, y: int, moving: str):
        self.x = x
        self.y = y
        self.d = moving  # NSEW, up to 3 times
        # self.weight = weight

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
        return f"({self.x},{self.y}):{self.score(self.x, self.y)} [{self.d}]"

    def backtrack(self, d: Literal["N", "S", "E", "W"]):
        if self.d == "":
            return False
        return "SNWE"["NSEW".index(self.d[-1])] == d

    def isvalid(self, x: int, y: int, d: Literal["N", "S", "E", "W"]):
        # print("isvalid", d, d + d, d * d)
        return (
            x >= 0
            and x < self.WIDTH
            and y >= 0
            and y < self.HEIGHT
            and self.d + d != d * 4
        )

    def atgoal(self) -> bool:
        return self.x == self.WIDTH - 1 and self.y == self.HEIGHT - 1

    @classmethod
    def score(cls, x: int, y: int) -> int:
        return cls.GRID[y * cls.WIDTH + x]

    def move(self, d: Literal["N", "S", "E", "W"]) -> tuple[int, int]:
        if d == "N":
            return (self.x, self.y - 1)
        if d == "S":
            return (self.x, self.y + 1)
        if d == "E":
            return (self.x + 1, self.y)
        return (self.x - 1, self.y)

    def spawn(self, d: Literal["N", "S", "E", "W"]):  # -> "Node" | None:
        x, y = self.move(d)
        if self.isvalid(x, y, d):
            if d in self.d:
                d = self.d + d
            # w = self.score(x, y) + self.weight
            return Node(x, y, d)
        return None


def part1(lines: list[str]) -> int:
    return Node.search(lines)


def part2(lines: list[str]) -> int:
    return 0


class TestDay17(unittest.TestCase):
    def test_1a(self):
        with open("./test17.txt", "r") as f:
            self.assertEqual(part1(list(f)), 102)

    # def test_1(self):
    #     with open("./input17.txt", "r") as f:
    #         self.assertEqual(part1(list(f)), 1260)

    # def test_2a(self):
    #     with open('./test17.txt', 'r') as f:
    #         self.assertEqual(part2(list(f)), None)

    # def test_2(self):
    #     with open('./input17.txt', 'r') as f:
    #         self.assertEqual(part2(list(f)), None)


if __name__ == "__main__":
    unittest.main()
