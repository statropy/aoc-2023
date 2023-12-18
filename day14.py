# day14.py 2023
import unittest


def makecubes(lines: list[str]) -> list[int]:
    # cubes = []
    # for line in lines:
    #     cubes.append(
    #         int(line.strip().replace("O", "0").replace(".", "0").replace("#", "1"), 2)
    #     )
    return [
        int(line.strip().replace("O", "0").replace(".", "0").replace("#", "1"), 2)
        for line in lines
    ]


def makerocks(lines: list[str]) -> list[int]:
    return [
        int(line.strip().replace("O", "1").replace(".", "0").replace("#", "0"), 2)
        for line in lines
    ]


def show(rocks, cubes, width):
    print()
    for y in range(len(rocks)):
        for x in range(width - 1, -1, -1):
            if cubes[y] & (1 << x) != 0 and rocks[y] & (1 << x) != 0:
                print("!", end="")
            elif cubes[y] & (1 << x) != 0:
                print("#", end="")
            elif rocks[y] & (1 << x) != 0:
                print("O", end="")
            else:
                print(".", end="")
        print(f" {len(rocks)-y:2}")


def part1(lines: list[str]) -> int:
    cubes = makecubes(lines)
    rocks = makerocks(lines)
    # print()
    # for i in range(len(lines)):
    #     print(
    #         f"{cubes[i]:03X} | {rocks[i]:03X} = {cubes[i]|rocks[i]:03X} {len(lines)-i:2}"
    #     )

    # i = 0
    # r0 = cubes[i] | rocks[i]
    # r1 = cubes[i + 1] | rocks[i + 1]
    # r0_new = r0 | rocks[i + 1]
    # r1_new = r1 & ~((r0 ^ rocks[i + 1]) & rocks[i + 1])  # | cubes[i + 1]
    # print()
    # # print(f"{r0:010b}")
    # # print(f"{r1:010b}")
    # # print("-" * 50)
    # # print(f"{r0_new:010b}")
    # # print(f"{r1_new:010b}")

    # r = [0, 0]
    # r[i] = rocks[i] | rocks[i + 1]
    # r[i + 1] = rocks[i + 1] & ~(((cubes[i] | rocks[i]) ^ rocks[i + 1]) & rocks[i + 1])
    # # rocks[i + 1] = (cubes[i] | rocks[i]) ^ rocks[i + 1]
    # print(f"{r[i]:010b}")
    # print(f"{r[i+1]:010b}")
    changed = True
    while changed:
        # show(rocks, cubes, len(lines[0].strip()))
        changed = False
        for i in range(len(lines) - 1):
            a = (rocks[i] | rocks[i + 1]) & ~(cubes[i])
            rocks[i + 1] = rocks[i + 1] & ~(
                ((cubes[i] | rocks[i]) ^ rocks[i + 1]) & rocks[i + 1]
            )
            if a != rocks[i]:
                changed = True
            rocks[i] = a

        # for i in range(len(lines)):
        #     print(f"{rocks[i]:010b} {len(lines)-i:2}")
    # s = 0
    # for y in range(len(rocks)):
    #     points = len(rocks)-y
    #     s += points * rocks[y].bit_count()

    return sum([(len(rocks) - y) * rocks[y].bit_count() for y in range(len(rocks))])


def part2(lines: list[str]) -> int:
    return 0


class TestDay14(unittest.TestCase):
    def test_1a(self):
        with open("./test14.txt", "r") as f:
            self.assertEqual(part1(list(f)), 136)

    def test_1(self):
        with open("./input14.txt", "r") as f:
            self.assertEqual(part1(list(f)), 108614)

    # def test_2a(self):
    #     with open('./test14.txt', 'r') as f:
    #         self.assertEqual(part2(list(f)), None)

    # def test_2(self):
    #     with open('./input14.txt', 'r') as f:
    #         self.assertEqual(part2(list(f)), None)


if __name__ == "__main__":
    unittest.main()
