# day23.py 2023
import unittest
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])


class Path(object):
    D = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    DIR1 = [D, [D[0]], [D[1]], [D[2]], [D[3]], []]
    DIR2 = [D, D, D, D, D, []]
    LANDS = ".<^>v#"

    def __init__(self, lines: list[str]):
        self.grid: list[str] = [line.strip() for line in lines]
        self.start: Point = Point(1, 0)
        self.end: Point = Point(len(self.grid[-1]) - 2, len(self.grid) - 1)
        # self.visited: dict[Point:int] = {}
        self.tovisit: list[tuple[Point, set[Point]]] = [(self.start, set())]

    def walk(self, part: int = 1):
        self.dir = self.DIR1
        if part == 2:
            self.dir = self.DIR2
        m = 0
        while len(self.tovisit) > 0:
            p, history = self.tovisit.pop(0)
            # print(p, len(history))
            if p.x == self.end.x and p.y == self.end.y:
                # print(len(history))
                m = max(m, len(history))
            # elif p in self.visited:
            #     self.visited[p] = max(steps, self.visited[p])
            else:
                history.add(p)
                self.tovisit += self.neighbors(p, history)
        # print(self.end)
        return m

    def land(self, p: Point):
        return self.grid[p.y][p.x]

    def isvalid(self, p: Point) -> bool:
        return (
            p.x >= 0
            and p.x < len(self.grid[0])
            and p.y >= 0
            and p.y < len(self.grid)
            and self.land(p) != "#"
        )

    def neighbors(self, p: Point, history: set[Point]):
        neighs = []
        for dx, dy in self.dir[self.LANDS.index(self.land(p))]:
            n = Point(p.x + dx, p.y + dy)
            if n not in history and self.isvalid(n):
                neighs.append(n)
        if len(neighs) == 0:
            return []
        alln = [(neighs[0], history)]
        for n in neighs[1:]:
            # print("Split!")
            alln.append((n, history.copy()))
        return alln


def part1(lines: list[str]) -> int:
    path = Path(lines)
    return path.walk()


def part2(lines: list[str]) -> int:
    path = Path(lines)
    return path.walk(2)


class TestDay23(unittest.TestCase):
    def test_1a(self):
        with open("./test23.txt", "r") as f:
            self.assertEqual(part1(list(f)), 94)

    def test_1(self):
        with open("./input23.txt", "r") as f:
            self.assertEqual(part1(list(f)), 2018)

    def test_2a(self):
        with open("./test23.txt", "r") as f:
            self.assertEqual(part2(list(f)), 154)

    def test_2(self):
        with open("./input23.txt", "r") as f:
            self.assertEqual(part2(list(f)), None)


if __name__ == "__main__":
    unittest.main()
