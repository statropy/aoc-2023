# day8.py 2023
import unittest
from math import lcm


def parse(lines: list[str]) -> tuple[str, dict]:
    dirint = {"L": 0, "R": 1}
    instructions = [dirint[d] for d in lines[0].strip()]
    seq = {
        k: (r.strip()[1:], l.strip()[:-1])
        for k, r, l in (
            [k.strip()] + rl.strip().split(",")
            for k, rl in (line.strip().split("=") for line in lines[2:])
        )
    }
    return instructions, seq


def part1(lines: list[str]) -> int:
    instructions, seq = parse(lines)
    steps = 0
    place = "AAA"
    while True:
        for dir in instructions:
            place = seq[place][dir]
            steps += 1
            if place == "ZZZ":
                return steps


def part2(lines):
    instructions, seq = parse(lines)
    nodes = [n for n in seq.keys() if n[2] == "A"]
    found = []
    for _ in nodes:
        found.append({})

    for i, node in enumerate(nodes):
        run = True
        step = 0
        while run:
            for dir in instructions:
                node = seq[node][dir]
                step += 1
                if node[2] == "Z":
                    if node in found[i].keys():
                        run = False
                        break
                    else:
                        found[i][node] = step

    return lcm(*[min(node.values()) for node in found])


class TestDay8(unittest.TestCase):
    def test_1a(self):
        with open("./test8.txt", "r") as f:
            self.assertEqual(part1(list(f)), 2)

    def test_1b(self):
        with open("./test8b.txt", "r") as f:
            self.assertEqual(part1(list(f)), 6)

    def test_1(self):
        with open("./input8.txt", "r") as f:
            self.assertEqual(part1(list(f)), 12737)

    def test_2a(self):
        with open("./test8c.txt", "r") as f:
            self.assertEqual(part2(list(f)), 6)

    def test_2(self):
        with open("./input8.txt", "r") as f:
            self.assertEqual(part2(list(f)), 9064949303801)


if __name__ == "__main__":
    unittest.main()
