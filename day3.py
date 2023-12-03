#day3.py 2023
import unittest
from math import prod
import re

class PartNumber(object):
    def __init__(self, lines: list[str], match:str):
        self.lines : list[str] = lines
        self.match = match
        self.symbols = self.getallcoords(match)

    def getallcoords(self, match:str) -> set:
        return {(r,c) for r,row in enumerate(self.lines) for c,ch in enumerate(row) if ch in match}
    
    def validcoord(self, r:int, c:int) -> bool:
        return r >=0 and r <len(self.lines) and c >= 0 and c < len(self.lines[r])
    
    def validdigit(self, r:int, c:int) -> bool:
       return self.validcoord(r,c) and self.lines[r][c].isdigit()

    def grabpn(self, r:int, c:int) -> None | int:
        return int(re.findall('\d+', self.lines[r][:c+1])[-1] + re.findall('\d+', self.lines[r][c:])[0][1:])

    def __iter__(self):
        for r,c in self.symbols:
            yield {self.grabpn(row, col) for row in range(r-1, r+2) for col in range(c-1, c+2) if self.validdigit(row,col)}

def solve(lines: list[str], match:str):
    return [{int(re.findall('\d+', lines[r][:c+1])[-1] + re.findall('\d+', lines[r][c:])[0][1:]) for r in range(row-1, row+2) for c in range(col-1, col+2) if (r >=0 and r <len(lines) and c >= 0 and c < len(lines[r])) and lines[r][c].isdigit()} for row,col in {(r,c) for r,row in enumerate(lines) for c,ch in enumerate(row) if ch in match}]

def part1(lines: list[str]):
    # return sum([sum(p) for p in PartNumber(lines, '+=-&#/*$%@')])
    return sum([sum(p) for p in solve(lines, '+=-&#/*$%@')])

def part2(lines):
    # return sum([prod(p) for p in PartNumber(lines, '*') if len(p) == 2])
    return sum([prod(p) for p in solve(lines, '*') if len(p) == 2])

class TestDay3(unittest.TestCase):
    def test_1a(self):
        with open('./test3.txt', 'r') as f:
            self.assertEqual(part1(list(f)), 4361)

    def test_1(self):
        with open('./input3.txt', 'r') as f:
            self.assertEqual(part1(list(f)), 532331)

    def test_2a(self):
        with open('./test3.txt', 'r') as f:
            self.assertEqual(part2(list(f)), 467835)

    def test_2(self):
        with open('./input3.txt', 'r') as f:
            self.assertEqual(part2(list(f)), 82301120)

if __name__ == '__main__':
    unittest.main()
