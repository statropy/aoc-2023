#day1.py 2022
import unittest

numbers = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

def get_digits(line):
    digits = [c for c in line if c.isdigit()]
    return int(digits[0]+digits[-1])

def part1(lines):
    return sum([get_digits(line) for line in lines])

def get_digit(line, front=True):
    idx = 0
    if not front:
        idx = -1

    while len(line) > 0:
        if line[idx].isdigit():
            return line[idx]
        for i,num in enumerate(numbers):
            if (front and line.startswith(num)) or (not front and line.endswith(num)):
                return str(i+1)
        if front:
            line = line[1:]
        else:
            line = line[:-1]

def get_digits_all(line):
    digits = []
    print(line[:-1], end=' = ')
    while len(line) > 0:
        if line[0].isdigit():
            digits += line[0]
        else:
            for i,num in enumerate(numbers):
                if line.startswith(num):
                    digits += str(i+1)
                    line = line[len(num)-1:]
                    break
        line = line[1:]
    print(int(digits[0]+digits[-1]))
    return int(digits[0]+digits[-1])

def part2(lines):
    return sum([int(get_digit(line) + get_digit(line, False)) for line in lines])

class TestDay1(unittest.TestCase):
    def test_1a(self):
        with open('./test1.txt', 'r') as f:
            self.assertEqual(part1(list(f)), 142)

    def test_1(self):
        with open('./input1.txt', 'r') as f:
            self.assertEqual(part1(list(f)), 56397)

    def test_2a(self):
        with open('./test1-2.txt', 'r') as f:
            self.assertEqual(part2(list(f)), 281)

    #55725 is too high
    def test_2(self):
        with open('./input1.txt', 'r') as f:
            self.assertEqual(part2(list(f)), 55701)

    #must search backward from end for second digit
    # def test_2_comp(self):
    #     with open('./input1.txt', 'r') as f:
    #         for line in f:
    #             a = get_digits_all(line)
    #             b = int(get_digit(line) + get_digit(line, False))
    #             self.assertEqual(a, b)

if __name__ == '__main__':
    unittest.main()
