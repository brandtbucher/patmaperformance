"""Classify poker hands.

This benchmark tests the performance of PEP 634's mapping patterns.
"""


import collections
import functools
import itertools
import random

import pyperf


class _Metadata:
    SUITS = "<suits>"


@functools.lru_cache(1)
def _get_stats(count: int | None = None) -> tuple[dict[str, int], ...]:
    """Generate "stats" for *count* diverse poker hands.

    These will be dicts containing the frequencies of present ranks, as well as
    the number of different suits.

    If *count* is None, generate stats for all valid hands (useful for testing).
    """
    cards = list(itertools.product("A23456789TJQK", "♠♡♢♣"))
    if count is None:
        hands = itertools.combinations(cards, 5)
    else:
        sample = random.Random(0).sample  # Deterministic!
        hands = (sample(cards, 5) for _ in range(count))
    all_stats = []
    for hand in hands:
        # zip(*iterable) is weird:
        # ("A", "♠"), ("2", "♡"), ("3", "♢"), ("4", "♣"), ("5", "♠")
        # -> ("A", "2", "3", "4", "5"), ("♠", "♡", "♢", "♣", "♠")
        ranks, suits = zip(*hand, strict=True)
        stats = dict.fromkeys(ranks, 0)
        for rank in stats:
            stats[rank] = ranks.count(rank)
        stats[_Metadata.SUITS] = len(set(suits))
        all_stats.append(stats)
    return tuple(all_stats)


def patma_holdem(count: int | None = None) -> tuple[float, dict[str, int]]:
    all_stats = _get_stats(count)
    results = collections.defaultdict(int)
    # Begin benchmark:
    start = pyperf.perf_counter()
    for stats in all_stats:
        match stats:
            case {_Metadata.SUITS: 1, "T": _, "J": _, "Q": _, "K": _, "A": _}:
                results["Royal Flush"] += 1
            case (
                {_Metadata.SUITS: 1, "A": _, "2": _, "3": _, "4": _, "5": _}
                | {_Metadata.SUITS: 1, "2": _, "3": _, "4": _, "5": _, "6": _}
                | {_Metadata.SUITS: 1, "3": _, "4": _, "5": _, "6": _, "7": _}
                | {_Metadata.SUITS: 1, "4": _, "5": _, "6": _, "7": _, "8": _}
                | {_Metadata.SUITS: 1, "5": _, "6": _, "7": _, "8": _, "9": _}
                | {_Metadata.SUITS: 1, "6": _, "7": _, "8": _, "9": _, "T": _}
                | {_Metadata.SUITS: 1, "7": _, "8": _, "9": _, "T": _, "J": _}
                | {_Metadata.SUITS: 1, "8": _, "9": _, "T": _, "J": _, "Q": _}
                | {_Metadata.SUITS: 1, "9": _, "T": _, "J": _, "Q": _, "K": _}
            ):
                results["Straight Flush"] += 1
            case {_Metadata.SUITS: 4, **ranks} if 4 in ranks.values():
                results["Four Of A Kind"] += 1
            case {_Metadata.SUITS: 4 | 3, **ranks} if len(ranks) == 2:
                results["Full House"] += 1
            case {_Metadata.SUITS: 1}:
                results["Flush"] += 1
            case (
                {"A": _, "2": _, "3": _, "4": _, "5": _}
                | {"2": _, "3": _, "4": _, "5": _, "6": _}
                | {"3": _, "4": _, "5": _, "6": _, "7": _}
                | {"4": _, "5": _, "6": _, "7": _, "8": _}
                | {"5": _, "6": _, "7": _, "8": _, "9": _}
                | {"6": _, "7": _, "8": _, "9": _, "T": _}
                | {"7": _, "8": _, "9": _, "T": _, "J": _}
                | {"8": _, "9": _, "T": _, "J": _, "Q": _}
                | {"9": _, "T": _, "J": _, "Q": _, "K": _}
                | {"T": _, "J": _, "Q": _, "K": _, "A": _}
            ):
                results["Straight"] += 1
            case {_Metadata.SUITS: 4 | 3, **ranks} if 3 in ranks.values():
                results["Three Of A Kind"] += 1
            case {_Metadata.SUITS: _, **ranks} if len(ranks) == 3:
                results["Two Pair"] += 1
            case {_Metadata.SUITS: _, **ranks} if 2 in ranks.values():
                results["One Pair"] += 1
            case _:
                results["High Card"] += 1
    return pyperf.perf_counter() - start, dict(results)


def bench_patma_holdem(count: int) -> float:
    return patma_holdem(count)[0]


if __name__ == "__main__":
    runner = pyperf.Runner()
    runner.metadata["description"] = "PEP 634 mapping patterns"
    runner.bench_time_func("patma_holdem", bench_patma_holdem)
