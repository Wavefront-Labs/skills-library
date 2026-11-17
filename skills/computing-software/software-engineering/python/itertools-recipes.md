---
id: computing-software.software-engineering.python.itertools-recipes
name: itertools-recipes
category: computing-software
field: software-engineering
product: python
tags: [python, py-iteration, itertools-recipes, itertools, batched, groupby, chain, pairwise, islice]
level: practitioner
status: docs-checked
description: "Use itertools for batching, windows, grouping, flattening and lazy pipelines: batched, pairwise, groupby, chain.from_iterable, islice, tee and accumulate."
sources: ["https://docs.python.org/3/library/itertools.html", "https://docs.python.org/3/library/itertools.html#itertools-recipes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# itertools recipes

```python
from itertools import batched, pairwise, chain, groupby, islice, accumulate, product, zip_longest
from operator import itemgetter

list(batched(range(7), 3))            # [(0,1,2),(3,4,5),(6,)]  -- 3.12+; strict=True in 3.13
list(pairwise("abcd"))                # [('a','b'),('b','c'),('c','d')]  -- 3.10+
list(chain.from_iterable([[1], [2, 3]]))   # flatten one level, lazily
first5 = list(islice(open_file_lines, 5)) # slice any iterator without loading it
list(accumulate([1, 2, 3, 4]))        # running sum [1, 3, 6, 10]

rows = sorted(records, key=itemgetter("team"))          # groupby needs sorted input
for team, grp in groupby(rows, key=itemgetter("team")):
    members = list(grp)               # consume the group before advancing
```

## Choosing
- Unknown-length chunks of a stream: `batched`. Before 3.12 loop with `while batch := tuple(islice(it, n)):` (the docs' equivalent code).
- Cartesian parameter grids: `product(a, b, repeat=2)`; combinations: `combinations`, `permutations`.
- Merge iterables of unequal length: `zip_longest(fillvalue=...)`.
- Unique-preserving order: the `unique_everseen` recipe from the docs.

## Gotchas
- Iterators are single-pass. `tee` may need significant auxiliary storage; if one iterator uses most of the data before another starts, use `list` instead. `tee` iterators are not thread-safe.
- `groupby` groups only *consecutive* equal keys, and the source is shared, so each group is invalidated when you advance to the next key.
- `itertools.batched` yields tuples, not lists, and the last batch may be shorter (`strict=True` raises `ValueError`).
- Infinite iterators (`count`, `cycle`, `repeat`) hang when passed to `list()`; bound them with `islice`/`takewhile`.

## Verify
- [ ] Doctest the recipe with a short input including an empty iterable and a length that is not a multiple of the batch size.

## Checked

- 2026-11-03: checked against the CPython docs `library/itertools.rst`: `batched` (3.12, `strict` 3.13, tuples), `pairwise` (3.10), `chain.from_iterable`, `islice`, `accumulate`, `groupby` consecutive keys and shared source, `tee` storage and thread-safety notes, the `unique_everseen` recipe, the `tuple(islice(...))` batching loop.
- Removed: `zip(strict=True)` version claim and `dict.fromkeys` advice (not on this page), `islice` skip remark, the tracemalloc check.

Method: documentation only; no commands were run.
