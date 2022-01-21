"""Build a red-black tree.

This benchmark tests the performance of PEP 634's class patterns.
"""
import random

import pyperf

SIZE = 1 << 13


class Node:
    __match_args__ = ("value", "left", "right")

    def __init__(self, value: int, left: "Node | None", right: "Node | None") -> None:
        self.value = value
        self.left = left
        self.right = right

    def add(self, value: int) -> "Node":
        match self._add(value):
            case Red(v, l, r):
                return Black(v, l, r)._rebalance()
            case node:
                return node

    def _add(self, value: int) -> "Node":
        match self:
            case Node(v, left=None, right=r) if value < v:
                return self.__class__(v, Red(value, None, None), r)
            case Node(v, left=l, right=None) if v <= value:
                return self.__class__(v, l, Red(value, None, None))
            case Red(v, left=l, right=r) if value < v:
                return Red(v, l._add(value), r)
            case Red(v, left=l, right=r) if v <= value:
                return Red(v, l, r._add(value))
            case Black(v, left=l, right=r) if value < v:
                return Black(v, l._add(value), r)._rebalance()
            case Black(v, left=l, right=r) if v <= value:
                return Black(v, l, r._add(value))._rebalance()
            case _:
                assert False, self

    def _rebalance(self) -> "Node":
        match self:
            case (
                Black(rv, Red(v, Red(lv, ll, lr), rl), rr)
                | Black(rv, Red(lv, ll, Red(v, lr, rl)), rr)
                | Black(lv, ll, Red(rv, Red(v, lr, rl), rr))
                | Black(lv, ll, Red(v, lr, Red(rv, rl, rr)))
            ):
                return Red(v, Black(lv, ll, lr), Black(rv, rl, rr))
            case _:
                return self


class Red(Node):
    pass


class Black(Node):
    pass


def bench_red_black(count: int) -> float:
    choices = random.Random(0).choices  # Deterministic!
    values = choices(range(SIZE), k=SIZE)
    root = Black(values.pop(), None, None)
    loops = range(count)
    # Begin benchmark:
    start = pyperf.perf_counter()
    for _ in loops:
        tree = root
        for value in values:
            tree = tree.add(value)
    return pyperf.perf_counter() - start


if __name__ == "__main__":
    runner = pyperf.Runner()
    runner.metadata["description"] = "PEP 634 class patterns"
    runner.bench_time_func("red_black", bench_red_black)
