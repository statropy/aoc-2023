# day7.py 2023
import unittest
from collections.abc import Callable

RANKS = {
    "A": 13,
    "K": 12,
    "Q": 11,
    "J": 10,
    "T": 9,
    "9": 8,
    "8": 7,
    "7": 6,
    "6": 5,
    "5": 4,
    "4": 3,
    "3": 2,
    "2": 1,
}
RANKS2 = {
    "A": 13,
    "K": 12,
    "Q": 11,
    "J": 0,
    "T": 9,
    "9": 8,
    "8": 7,
    "7": 6,
    "6": 5,
    "5": 4,
    "4": 3,
    "3": 2,
    "2": 1,
}


def findtype(hand: str) -> int:
    uniques = set(hand)

    if len(uniques) == 5:
        return 1  # high card
    if len(uniques) == 4:
        return 2  # 1 pair
    if len(uniques) == 1:
        return 7  # five of a kind

    counts = {hand.count(card) for card in uniques}
    if 4 in counts:
        return 6  # four of a kind 4,1
    if 3 in counts:
        if 2 in counts:
            return 5  # full house 3,2
        else:
            return 4  # three of a kind 3,1
    return 3  # two pair 2, 1


def findtypewild(hand: str, wild: str) -> int:
    numwild = hand.count(wild)
    if numwild == 0:
        return findtype(hand)
    if numwild == 4 or numwild == 5:
        return 7  # five of a kind
    uniques = set(hand)
    if len(uniques) == 2:  # wwwAA or wwAAA or wAAAA
        return 7  # five of a kind
    if numwild == 3:  # wwwAB
        return 6  # four of a kind
    if numwild == 2:
        if len(uniques) == 3:  # wwAAB
            return 6  # four of a kind
        else:  # wwABC
            return 4  # three of a kind
    i = hand.index("J")
    return max([findtype(hand[:i] + card + hand[i + 1 :]) for card in RANKS.keys()])


def score2(hand: str) -> int:
    rank = findtypewild(hand, "J")
    for c in hand:
        rank = (rank << 4) + RANKS2[c]
    return rank


def score1(hand: str) -> int:
    rank = findtype(hand)
    for c in hand:
        rank = (rank << 4) + RANKS[c]
    return rank


def score(lines: list[str], key: Callable[[str], int]) -> int:
    bids = {h: int(b) for h, b in (line.split() for line in lines)}
    hands = sorted(bids.keys(), key=key)
    return sum([(i + 1) * bids[hand] for i, hand in enumerate(hands)])


def part1(lines: list[str]) -> int:
    return score(lines, score1)


def part2(lines: list[str]) -> int:
    return score(lines, score2)


class TestDay7(unittest.TestCase):
    def test_1a(self):
        with open("./test7.txt", "r") as f:
            self.assertEqual(part1(list(f)), 6440)

    def test_1(self):
        with open("./input7.txt", "r") as f:
            self.assertEqual(part1(list(f)), 251058093)

    def test_2a(self):
        with open("./test7.txt", "r") as f:
            self.assertEqual(part2(list(f)), 5905)

    def test_2(self):
        with open("./input7.txt", "r") as f:
            self.assertEqual(part2(list(f)), 249781879)


if __name__ == "__main__":
    unittest.main()
