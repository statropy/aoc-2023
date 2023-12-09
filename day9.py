# day9.py 2023
import unittest
from typing import Literal


def descend(seq: list[int], method: Literal["front", "end"]) -> int:
    if len(seq) == seq.count(seq[0]):
        return seq[0]
    d = descend([seq[i] - seq[i - 1] for i in range(1, len(seq))], method)
    if method == "end":
        return seq[-1] + d
    elif method == "front":
        return seq[0] - d
    else:
        raise ValueError(f'invalid method "{method}"')


def run(lines: list[str], method: Literal["front", "end"]) -> int:
    return sum([descend([int(x) for x in line.split()], method) for line in lines])


def part1(lines: list[str]) -> int:
    return run(lines, "end")


def part2(lines: list[str]) -> int:
    return run(lines, "front")


class TestDay9(unittest.TestCase):
    def test_1a(self):
        with open("./test9.txt", "r") as f:
            self.assertEqual(part1(list(f)), 114)

    def test_1(self):
        with open("./input9.txt", "r") as f:
            self.assertEqual(part1(list(f)), 1938731307)

    def test_2a(self):
        with open("./test9.txt", "r") as f:
            self.assertEqual(part2(list(f)), 2)

    def test_2(self):
        with open("./input9.txt", "r") as f:
            self.assertEqual(part2(list(f)), 948)


if __name__ == "__main__":
    unittest.main()
