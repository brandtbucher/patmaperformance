The PEP 634 Benchmark Suite
===========================

This project is a testing ground for the development of benchmarks for
[PEP 634](https://www.python.org/dev/peps/pep-0634)'s structural pattern
matching implementation.  The goal is to ultimately have them incorporated into
[the Python benchmark suite](https://github.com/python/pyperformance).

Running these benchmarks requires Python 3.10.0a6 or greater with `pyperf`
installed.  Tests can be run with `pytest`.


`bm_holdem.py`
--------------

Classify poker hands.

This benchmark tests the performance of PEP 634's mapping patterns.


`bm_rbtree.py`
--------------

Build a red-black tree.

This benchmark tests the performance of PEP 634's class patterns.