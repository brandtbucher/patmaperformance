"""Evaluate the Ackermann function.

This benchmark tests the performance of PEP 634's sequence patterns.
"""
import pyperf

M = 1 << 1
N = 1 << 9


def ackermann(m: int, n: int) -> int:
    assert 0 <= m, m
    assert 0 <= n, n
    stack = [m, n]
    while True:
        match stack:
            case [*_, 0, n]:
                stack[-2:] = [n + 1]
            case [*_, m, 0]:
                stack[-2:] = [m - 1, 1]
            case [*_, m, n]:
                stack[-2:] = [m - 1, m, n - 1]
            case [a]:
                return a
            case stack:
                assert False, stack


def bench_ackermann(count: int) -> float:
    loops = range(count)
    # Begin benchmark:
    start = pyperf.perf_counter()
    for _ in loops:
        ackermann(M, N)
    return pyperf.perf_counter() - start


if __name__ == "__main__":
    runner = pyperf.Runner()
    runner.metadata["description"] = "PEP 634 sequence patterns"
    runner.bench_time_func("ackermann", bench_ackermann)
