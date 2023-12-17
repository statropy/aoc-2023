# day13.py 2023
import unittest


class PatternGenerator(object):
    def __init__(self, lines: list[str]) -> list[str]:
        self.lines = lines

    def __iter__(self):
        tosend = []
        for line in self.lines:
            if line[0] == "\n":
                yield tosend
                tosend = []
            else:
                tosend.append(line.strip())
        yield tosend


class XorGenerator(object):
    def __init__(self, rows: list[int]):
        self.rows = rows

    def __iter__(self):
        for j, left in enumerate(self.rows[:-1]):
            for k, right in enumerate(self.rows[j + 1 :]):
                xor = left ^ right
                if xor.bit_count() == 1:
                    for idx, val in ((j, left), (j + 1 + k, right)):
                        test = self.rows.copy()
                        test[idx] = val ^ xor
                        yield test


def rowsum(row: str):
    z = 0
    for i, c in enumerate(row):
        if c == "#":
            z |= 1 << i
    return z


def colsum(lines: list[str], x: int):
    z = 0
    for y in range(len(lines)):
        if lines[y][x] == "#":
            z |= 1 << y
    return z


def testreflect(rows):
    found = set()
    for i, row in enumerate(rows[1:]):
        if row == rows[i]:
            reflect = True
            right = i + 1
            to_match = min(len(rows) - right, right)
            lrows = rows[right - to_match : right]
            rrows = rows[right : right + to_match]
            for k in range(to_match):
                if lrows[-(k + 1)] != rrows[k]:
                    reflect = False
                    break
            if reflect:
                found.add(right)
    return found


def reflect(lines: list[str], method=testreflect):
    z = method([colsum(lines, x) for x in range(len(lines[0]))])
    if len(z) == 0:
        z = method([rowsum(row) for row in lines])
        return z.pop() * 100
    return z.pop()


def part1(lines: list[str]) -> int:
    return sum([reflect(pattern) for pattern in PatternGenerator(lines)])


def smudge(rows: list[int]) -> int | None:
    allfound = set()
    exclude = testreflect(rows)
    for test in XorGenerator(rows):
        z = testreflect(test)
        for x in z:
            allfound.add(x)
    return allfound, exclude


def reflect2(lines: list[str]):
    rowfound, rowexclude = smudge([rowsum(row) for row in lines])
    colfound, colexclude = smudge([colsum(lines, x) for x in range(len(lines[0]))])

    r: set = rowfound - rowexclude
    c: set = colfound - colexclude
    if len(r) == 1:
        return r.pop() * 100
    return c.pop()


def part2(lines: list[str]) -> int:
    return sum([reflect2(pattern) for pattern in PatternGenerator(lines)])


class TestDay13(unittest.TestCase):
    def test_1a(self):
        with open("./test13.txt", "r") as f:
            self.assertEqual(part1(list(f)), 405)

    def test_1(self):
        with open("./input13.txt", "r") as f:
            self.assertEqual(part1(list(f)), 39939)

    def test_2a(self):
        with open("./test13.txt", "r") as f:
            self.assertEqual(part2(list(f)), 400)

    def test_2(self):
        with open("./input13.txt", "r") as f:
            self.assertEqual(part2(list(f)), 32069)


if __name__ == "__main__":
    unittest.main()
