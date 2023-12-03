#day2.py 2023
import unittest
from math import prod

def check1(line: str):
    bag = {'red':12, 'green':13, 'blue':14}
    game_str, record = line.strip().split(':')
    _, game = game_str.split(' ')
    game = int(game)
    runs = record.split(';')
    for run in runs:
        for grab in run.split(','):
            num, color = grab.strip().split(' ')
            num = int(num)
            if num > bag[color]:
                return 0
    return game

def check2(line:str) -> int:
    bag = {'red':0, 'blue':0, 'green':0}
    _, record = line.strip().split(':')
    runs = record.split(';')
    for run in runs:
        for grab in run.split(','):
            num, color = grab.strip().split(' ')
            num = int(num)
            bag[color] = max(bag[color], num)
    return prod(bag.values())

def part1(lines):
    return sum([check1(line) for line in lines])

def part2(lines):
    return sum([check2(line) for line in lines])

class TestDay2(unittest.TestCase):
    def test_1a(self):
        with open('./test2.txt', 'r') as f:
            self.assertEqual(part1(list(f)), 8)

    def test_1(self):
        with open('./input2.txt', 'r') as f:
            self.assertEqual(part1(list(f)), 2476)

    def test_2a(self):
        with open('./test2.txt', 'r') as f:
            self.assertEqual(part2(list(f)), 2286)

    def test_2(self):
        with open('./input2.txt', 'r') as f:
            self.assertEqual(part2(list(f)), 54911)

if __name__ == '__main__':
    unittest.main()
