# day6.py 2023
import unittest
from math import sqrt, ceil, floor, prod


def quadsolve(a, b, c):
    z = sqrt(b * b - 4 * a * c)
    return ((-b + z) / (2 * a), (-b - z) / (2 * a))


def findrange(t, d):
    roots = quadsolve(-1, t, d)
    if roots[0] > roots[1]:
        roots[0], roots[1] = roots[1], roots[0]
    low, high = floor(roots[0] + 1), ceil(roots[1] - 1)
    return high - low + 1


def part1(lines):
    return prod(
        [
            findrange(t, d)
            for t, d in [
                (int(x), -int(y))
                for x, y in list(zip(*[line.split(":")[1].split() for line in lines]))
            ]
        ]
    )


def part2(lines):
    t, d = ["".join(line.split(":")[1].split()) for line in lines]
    return findrange(int(t), -int(d))


class TestDay6(unittest.TestCase):
    def test_1a(self):
        with open("./test6.txt", "r") as f:
            self.assertEqual(part1(list(f)), 288)

    def test_1(self):
        with open("./input6.txt", "r") as f:
            self.assertEqual(part1(list(f)), 2269432)

    def test_2a(self):
        with open("./test6.txt", "r") as f:
            self.assertEqual(part2(list(f)), 71503)

    def test_2(self):
        with open("./input6.txt", "r") as f:
            self.assertEqual(part2(list(f)), 35865985)


if __name__ == "__main__":
    unittest.main()
