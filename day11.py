# day11.py 2023
import unittest


def total_distance(galaxies: list[tuple[int, int]]):
    distances: int = []
    for i, this in enumerate(galaxies[:-1]):
        for j, other in enumerate(galaxies[i + 1 :]):
            distances.append(
                int(abs(other[0] - this[0])) + int(abs(other[1] - this[1]))
            )
    return sum(distances)


def galaxy_distance(lines: list[str], scale: int = 2) -> int:
    width: int = len(lines[0].strip())
    empty_row_count: int = 0
    empty_cols: list[int] = []
    galaxies: list[tuple[int, int]] = []

    for col in range(width):
        transform = [row[col] for row in lines]
        if transform.count("#") == 0:
            empty_cols.append(col)

    for r, row in enumerate(lines):
        row = row.strip()
        c = row.find("#")
        if c == -1:
            empty_row_count += 1
            continue
        while c >= 0:
            leftcols = len([ec for ec in empty_cols if ec < c])
            galaxies.append(
                ((empty_row_count * (scale - 1)) + r, c + (leftcols * (scale - 1)))
            )
            c = row.find("#", c + 1)

    return total_distance(galaxies)


class TestDay11(unittest.TestCase):
    def test_1a(self):
        with open("./test11.txt", "r") as f:
            self.assertEqual(galaxy_distance(list(f)), 374)

    def test_1(self):
        with open("./input11.txt", "r") as f:
            self.assertEqual(galaxy_distance(list(f)), 9724940)

    def test_2a(self):
        with open("./test11.txt", "r") as f:
            self.assertEqual(galaxy_distance(list(f), scale=10), 1030)

    def test_2b(self):
        with open("./test11.txt", "r") as f:
            self.assertEqual(galaxy_distance(list(f), scale=100), 8410)

    def test_2(self):
        with open("./input11.txt", "r") as f:
            self.assertEqual(galaxy_distance(list(f), 1000000), 569052586852)


if __name__ == "__main__":
    unittest.main()
