---
id: computing-software.software-engineering.python.cpython-performance-idioms
name: cpython-performance-idioms
category: computing-software
field: software-engineering
product: python
tags: [python, python-performance-idioms, comprehensions, str-join, set-membership, generator-expressions, python-performance]
level: practitioner
status: verified
description: "Pure-Python speedups that matter after profiling: right data structures, comprehensions, str.join, avoiding repeated attribute lookups, builtins, generators and batching I/O."
sources: ["https://wiki.python.org/moin/TimeComplexity", "https://docs.python.org/3/faq/programming.html#performance", "https://docs.python.org/3/whatsnew/3.11.html#faster-cpython"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CPython performance idioms

**Goal:** the cheap, readable changes that make hot Python code several times faster,
applied only where a profiler pointed.

## 1. Data structure choice (biggest wins)
| Operation | list | set/dict | deque |
|---|---|---|---|
| `x in c` | O(n) | O(1) | O(n) |
| append/pop at end | O(1) | - | O(1) |
| insert/pop at front | O(n) | - | O(1) |
```python
allowed = set(allowed_ids)           # build once, then `if uid in allowed` in the loop
from collections import deque, Counter, defaultdict
counts = Counter(words)              # beats manual dict counting
```
`bisect` for sorted lookups, `heapq` for top-k (`heapq.nlargest(10, items, key=...)`).

## 2. Push loops into C
```python
total = sum(x.price for x in items)              # vs manual accumulation
names = [u.name for u in users if u.active]      # comprehension: faster than append loop
s = "".join(parts)                               # O(n); `s += part` in a loop is slower (CPython often optimises it to near-linear, but that is not guaranteed on other implementations)
m = max(items, key=attrgetter("score"))
any(p.match(line) for p in patterns)             # short-circuits
```
`map`/`filter` with a builtin or `operator` function are fast; with a lambda they are no
faster than a comprehension.

## 3. Reduce per-iteration overhead
```python
append = out.append                  # hoist attribute lookups out of very hot loops
pat = re.compile(r"...")             # compile once (re caches, but lookup isn't free)
for i, (a, b) in enumerate(zip(xs, ys)): ...   # no index arithmetic
```
Since 3.11 the specialising interpreter made many micro-tricks less important; measure
before uglifying code.

## 4. Avoid needless work
- Generators for pipelines over large data (`sum(1 for _ in f)`) to keep memory flat.
- `dict.get`/`setdefault`/`defaultdict` instead of try/except in hot loops where misses are common
  (exceptions are cheap only when rare).
- Batch I/O: one `executemany`, one bulk HTTP call, buffered file writes - I/O dominates
  most "slow Python" reports.
- Exit early; cache results (`functools.cache`).

## 5. When idioms are not enough
Vectorise with NumPy/pandas/polars, move the hot loop to Cython/Rust (PyO3), or use
multiprocessing. Try a newer CPython first: 3.11 alone was 10-60% faster than 3.10 on its release notes (1.25x average on pyperformance).

## Verify
- [ ] Each change justified by a profile (cProfile/py-spy) and a before/after benchmark.
- [ ] Readability kept: no micro-optimisations outside measured hot spots.

## Checked
- Python 3.14.0 timeit: `''.join` of 1000 parts 0.0044 s vs `+=` loop 0.167 s (per 2000 runs); `+=` scaled linearly 50k to 200k parts; `map(lambda)` 0.27 s vs comprehension 0.13 s; `in` on 1000-item list 0.125 s vs set 0.0006 s; dict miss via try/except 5x slower than hit, `.get` as fast as a hit. 3.11 speedup figure (10-60%, 1.25x average) read from the What's New in 3.11 page.
