import hypothesis

import bm_ackermann


@hypothesis.given(n=hypothesis.infer)
def test_ackermann_0(n: int) -> None:
    hypothesis.assume(0 <= n)
    assert bm_ackermann.ackermann(0, n) == n + 1


@hypothesis.given(n=hypothesis.infer)
def test_ackermann_1(n: int) -> None:
    hypothesis.assume(0 <= n < 1 << 16)
    assert bm_ackermann.ackermann(1, n) == n + 2


@hypothesis.given(n=hypothesis.infer)
def test_ackermann_2(n: int) -> None:
    hypothesis.assume(0 <= n < 1 << 8)
    assert bm_ackermann.ackermann(2, n) == 2 * n + 3


@hypothesis.given(n=hypothesis.infer)
def test_ackermann_3(n: int) -> None:
    hypothesis.assume(0 <= n < 1 << 2)
    assert bm_ackermann.ackermann(3, n) == 2 ** (n + 3) - 3
