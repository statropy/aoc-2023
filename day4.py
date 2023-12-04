#day4.py 2023
import unittest

def winners(line):
    left, numbers = line.strip().split('|')
    numbers = [int(x) for x in numbers.split()]
    card, winning = left.split(':')
    card = int(card.split()[1])
    winning = {int(x) for x in winning.split()}
    return len([x for x in numbers if x in winning])

def points1(wins):
    return 2**(wins-1) if wins > 0 else 0

def part1(lines):
    return sum([points1(winners(line)) for line in lines])

def part2(lines):
    wins = [winners(line) for line in lines]
    totals = [1]*len(wins)
    for card in range(len(wins)):
        for i in range(card+1, card+1+wins[card]):
            if i < len(wins):
                totals[i] += totals[card]
    return sum(totals)

class TestDay4(unittest.TestCase):
    def test_1a(self):
        with open('./test4.txt', 'r') as f:
            self.assertEqual(part1(list(f)), 13)

    def test_1(self):
        with open('./input4.txt', 'r') as f:
            self.assertEqual(part1(list(f)), 21568)

    def test_2a(self):
        with open('./test4.txt', 'r') as f:
            self.assertEqual(part2(list(f)), 30)

    def test_2(self):
        with open('./input4.txt', 'r') as f:
            self.assertEqual(part2(list(f)), 11827296)

if __name__ == '__main__':
    unittest.main()
