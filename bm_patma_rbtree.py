"""Build a red-black tree.

This benchmark tests the performance of PEP 634's class patterns.
"""


import random
import typing

import pyperf


class Node(typing.NamedTuple):

    value: int
    left: typing.Optional["Node"] = None
    right: typing.Optional["Node"] = None

    def add(self, value: int) -> "Node":
        match self._add(value):
            case Red(v, l, r):
                node = Black(v, l, r)
                return node._rebalance()
            case node:
                return node

    def _add(self, value: int) -> "Node":
        match self:
            case Node(v, left=None) if value < v:
                left = Red(value)
                return self._replace(left=left)
            case Node(v, right=None) if v <= value:
                right = Red(value)
                return self._replace(right=right)
            case Red(v, left=l) if value < v:
                left = l._add(value)
                return self._replace(left=left)
            case Red(v, right=r) if v <= value:
                right = r._add(value)
                return self._replace(right=right)
            case Black(v, left=l) if value < v:
                left = l._add(value)
                node = self._replace(left=left)
                return node._rebalance()
            case Black(v, right=r) if v <= value:
                right = r._add(value)
                node = self._replace(right=right)
                return node._rebalance()
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


def patma_rbtree(count: int) -> tuple[float, Node | None]:
    choices = random.Random(0).choices  # Deterministic!
    values = iter(choices(range(count), k=count))
    tree = Black(next(values))
    # Begin benchmark:
    start = pyperf.perf_counter()
    for value in values:
        tree = tree.add(value)
    return pyperf.perf_counter() - start, tree


def bench_patma_rbtree(count: int) -> float:
    return patma_rbtree(count)[0]


if __name__ == "__main__":
    runner = pyperf.Runner()
    runner.metadata["description"] = "PEP 634 class patterns"
    runner.bench_time_func("patma_rbtree", bench_patma_rbtree)
