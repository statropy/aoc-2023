# day5.py 2023
import unittest
from collections import namedtuple
from itertools import pairwise


def convert(seeds: list[int], lines: list[str]):
    Conv = namedtuple("Conv", ["dest", "source", "length"])

    converts: list[Conv] = []

    while len(lines) > 0:
        line = lines.pop(0)
        if line[0].isdigit():
            converts.append(Conv(*[int(x) for x in line.split()]))
        elif len(converts) == 0:
            continue
        else:
            break

    result = seeds.copy()
    for i, seed in enumerate(seeds):
        for conv in converts:
            if seed >= conv.source and seed < conv.source + conv.length:
                result[i] = conv.dest + (seed - conv.source)
                continue

    return (result, lines)


def part1(lines):
    seeds = [int(x) for x in lines[0].split(":")[1].split()]
    remaining = lines[1:]
    while len(remaining) > 0:
        seeds, reminaing = convert(seeds, remaining)

    return min(seeds)


def part2(lines):
    seeds = []
    seedlings = [int(x) for x in lines[0].split(":")[1].split()]
    for i in range(len(seedlings) >> 1):
        seeds += list(range(seedlings[i * 2], seedlings[i * 2] + seedlings[i * 2 + 1]))
    # print(len(seeds))
    remaining = lines[1:]
    while len(remaining) > 0:
        seeds, reminaing = convert(seeds, remaining)

    return min(seeds)


class TestDay5(unittest.TestCase):
    def test_1a(self):
        with open("./test5.txt", "r") as f:
            self.assertEqual(part1(list(f)), 35)

    def test_1(self):
        with open("./input5.txt", "r") as f:
            self.assertEqual(part1(list(f)), 227653707)

    def test_2a(self):
        with open("./test5.txt", "r") as f:
            self.assertEqual(part2(list(f)), 46)

    # def test_2(self):
    #     with open('./input5.txt', 'r') as f:
    #         self.assertEqual(part2(list(f)), None)


if __name__ == "__main__":
    unittest.main()
