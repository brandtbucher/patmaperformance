"""Classify poker hands.

This benchmark tests the performance of PEP 634's mapping patterns.
"""


import collections
import itertools

import pyperf


POSSIBLE_HANDS = 2_598_960  # 52 choose 5


class _Metadata:
    SUITS = ".suits"


def holdem(count: int) -> tuple[float, collections.Counter[str]]:
    # Generate stats for *count* diverse poker hands:
    cards = itertools.product("A23456789TJQK", "♠♡♢♣")
    step = POSSIBLE_HANDS // count or 1
    # Downsample by slicing when count is smaller than POSSIBLE_HANDS (likely):
    hands = itertools.islice(itertools.combinations(cards, 5), None, None, step)
    # Get the "stats" for each hand. This will be a Counter containing the
    # frequencies of present ranks, as well as the number of different suits:
    all_stats = []
    for hand in hands:
        # zip(*iterable) is weird:
        # ("A", "♠"), ("2", "♡"), ("3", "♢")
        # -> ("A", "2", "3"), ("♠", "♡", "♢")
        ranks, suits = zip(*hand, strict=True)
        stats = collections.Counter(ranks)
        stats[_Metadata.SUITS] = len(set(suits))
        all_stats.append(stats)
    # Repeat/trim all_stats as needed to reach the desired length:
    extra = all_stats[:count % len(all_stats)]
    all_stats *= count // len(all_stats)
    all_stats += extra
    assert len(all_stats) == count
    results = collections.defaultdict(int)
    # Begin benchmark:
    start = pyperf.perf_counter()
    for stats in all_stats:
        match stats:
            case {_Metadata.SUITS: 1, "T": _, "J": _, "Q": _, "K": _, "A": _}:
                results["Royal Flush"] += 1
            case ({_Metadata.SUITS: 1, "A": _, "2": _, "3": _, "4": _, "5": _} |
                  {_Metadata.SUITS: 1, "2": _, "3": _, "4": _, "5": _, "6": _} |
                  {_Metadata.SUITS: 1, "3": _, "4": _, "5": _, "6": _, "7": _} |
                  {_Metadata.SUITS: 1, "4": _, "5": _, "6": _, "7": _, "8": _} |
                  {_Metadata.SUITS: 1, "5": _, "6": _, "7": _, "8": _, "9": _} |
                  {_Metadata.SUITS: 1, "6": _, "7": _, "8": _, "9": _, "T": _} |
                  {_Metadata.SUITS: 1, "7": _, "8": _, "9": _, "T": _, "J": _} |
                  {_Metadata.SUITS: 1, "8": _, "9": _, "T": _, "J": _, "Q": _} |
                  {_Metadata.SUITS: 1, "9": _, "T": _, "J": _, "Q": _, "K": _}):
                results["Straight Flush"] += 1
            case {_Metadata.SUITS: 4, **ranks} if 4 in ranks.values():
                results["Four Of A Kind"] += 1
            case {_Metadata.SUITS: 4 | 3, **ranks} if len(ranks) == 2:
                results["Full House"] += 1
            case {_Metadata.SUITS: 1}:
                results["Flush"] += 1
            case ({"A": _, "2": _, "3": _, "4": _, "5": _} |
                  {"2": _, "3": _, "4": _, "5": _, "6": _} |
                  {"3": _, "4": _, "5": _, "6": _, "7": _} |
                  {"4": _, "5": _, "6": _, "7": _, "8": _} |
                  {"5": _, "6": _, "7": _, "8": _, "9": _} |
                  {"6": _, "7": _, "8": _, "9": _, "T": _} |
                  {"7": _, "8": _, "9": _, "T": _, "J": _} |
                  {"8": _, "9": _, "T": _, "J": _, "Q": _} |
                  {"9": _, "T": _, "J": _, "Q": _, "K": _} |
                  {"T": _, "J": _, "Q": _, "K": _, "A": _}):
                results["Straight"] += 1
            case {_Metadata.SUITS: 4 | 3, **ranks} if 3 in ranks.values():
                results["Three Of A Kind"] += 1
            case {_Metadata.SUITS: _, **ranks} if len(ranks) == 3:
                results["Two Pair"] += 1
            case {_Metadata.SUITS: _, **ranks} if 2 in ranks.values():
                results["One Pair"] += 1
            case _:
                results["High Card"] += 1
    return pyperf.perf_counter() - start, results


def bench_holdem(count: int) -> float:
    return holdem(count)[0]


if __name__ == "__main__":
    runner = pyperf.Runner()
    runner.metadata['description'] = "PEP 634 mapping patterns"
    runner.bench_time_func('holdem', bench_holdem)
