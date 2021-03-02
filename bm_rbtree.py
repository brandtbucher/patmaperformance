"""Build a red-black tree.

This benchmark tests the performance of PEP 634's class patterns.
"""


import random
import typing

import pyperf


class Node(typing.NamedTuple):

    value: int
    left: Node | None = None
    right: Node | None = None

    def add(self, value: int) -> Node:
        match self._add(value):
            case Red(v, left, right):
                return Black(v, left, right)._rebalance()
            case node:
                return node

    def _add(self, value: int) -> Node:
        match self:
            case Node(v, left=None) if value < v:
                return self._replace(left=Red(value))
            case Node(v, right=None) if v <= value:
                return self._replace(right=Red(value))
            case Red(v, left=left) if value < v:
                return self._replace(left=left._add(value))
            case Red(v, right=right) if v <= value:
                return self._replace(right=right._add(value))
            case Black(v, left=left) if value < v:
                return self._replace(left=left._add(value))._rebalance()
            case Black(v, right=right) if v <= value:
                return self._replace(right=right._add(value))._rebalance()

    def _rebalance(self) -> Node:
        match self:
            case (Black(rv, Red(v, Red(lv, ll, lr), rl), rr) |
                  Black(rv, Red(lv, ll, Red(v, lr, rl)), rr) |
                  Black(lv, ll, Red(rv, Red(v, lr, rl), rr)) |
                  Black(lv, ll, Red(v, lr, Red(rv, rl, rr)))):
                return Red(v, Black(lv, ll, lr), Black(rv, rl, rr))
            case _:
                return self


class Red(Node):
    pass


class Black(Node):
    pass


def rbtree(count: int) -> tuple[float, Node | None]:
    values = list(range(count))
    random.Random(0).shuffle(values)
    root, *values = values
    tree = Black(root)
    # Begin benchmark:
    start = pyperf.perf_counter()
    for value in values:
        tree = tree.add(value)
    return pyperf.perf_counter() - start, tree


def bench_rbtree(count: int) -> float:
    return rbtree(count)[0]


if __name__ == "__main__":
    runner = pyperf.Runner()
    runner.metadata['description'] = "PEP 634 class patterns"
    runner.bench_time_func('rbtree', bench_rbtree)
