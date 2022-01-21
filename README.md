The PEP 634 Benchmark Suite
===========================

This project is a testing ground for the development of benchmarks for
[PEP 634](https://www.python.org/dev/peps/pep-0634)'s structural pattern
matching implementation.  The goal is to ultimately have them incorporated into
[the Python benchmark suite](https://github.com/python/pyperformance).

Running these benchmarks requires Python 3.10.0a6 or greater with `pyperf`
installed.  Tests can be run with `pytest` and `hypothesis`.


Benchmarks
----------

### `bm_patma_ackermann.py`

Evaluate the Ackermann function.

This benchmark tests the performance of PEP 634's sequence patterns.


### `bm_patma_red_black.py`

Build a red-black tree.

This benchmark tests the performance of PEP 634's class patterns.
