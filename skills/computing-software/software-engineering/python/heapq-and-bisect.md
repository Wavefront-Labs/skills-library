---
id: computing-software.software-engineering.python.heapq-and-bisect
name: heapq-and-bisect
category: computing-software
field: software-engineering
product: python
tags: [python, py-collections, heapq-bisect, heapq, bisect, priority-queue, sorted-insert, top-n]
level: practitioner
status: docs-checked
description: "Priority queues and sorted lists with heapq and bisect: top-N, k-way merge, tie-breaking tuples, lazy deletion and binary search with key functions."
sources: ["https://docs.python.org/3/library/heapq.html", "https://docs.python.org/3/library/bisect.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# heapq and bisect

## heapq: a min-heap on a plain list
```python
import heapq, itertools
h = []
heapq.heappush(h, (2, "b")); heapq.heappush(h, (1, "a"))
heapq.heappop(h)                    # (1, 'a'): smallest first
heapq.nlargest(3, data, key=len)    # top-N without sorting everything
heapq.merge(sorted_a, sorted_b)     # lazy k-way merge of sorted inputs
heapq.heapify(lst)                  # O(n) in place
heapq.heappushpop(h, x)             # push then pop, faster than two calls

# Max-heap: negate numbers, or store (-priority, ...). Python 3.14 adds heapq.*_max functions.
# Tie-break so uncomparable payloads never get compared:
counter = itertools.count()
heapq.heappush(h, (prio, next(counter), task))
```
Update/cancel: mark entries removed (lazy deletion) and skip them on pop; there is no decrease-key.

## bisect: binary search in sorted sequences
```python
import bisect
grades = [60, 70, 80, 90]
"FDCBA"[bisect.bisect(grades, 85)]         # 'B'  -- bisect_right
i = bisect.bisect_left(a, x); found = i < len(a) and a[i] == x
bisect.insort(a, x)                         # O(n) insert, keeps order
bisect.bisect_left(rows, 5, key=lambda r: r.id)   # key= since 3.10
```

## Gotchas
- A heap is only partially ordered: `h[0]` is the minimum, but iterating `h` is not sorted.
- Pushing items with equal priorities and non-comparable payloads raises `TypeError` at the first tie.
- `insort` into a list is O(n) because the insertion step dominates the logarithmic search; for heavy insertion consider a heap.
- bisect on an unsorted list returns garbage, silently.

## Verify
- [ ] Test equal-priority pushes pop in insertion order (counter tie-breaker).
- [ ] Cross-check `nlargest(k, xs) == sorted(xs, reverse=True)[:k]` on random data.

## Checked

- 2026-11-03: checked against the CPython docs `library/heapq.rst` and `library/bisect.rst`: `_max` functions new in 3.14, tuple priorities with a counter tie-breaker, lazy removal of entries, `key` parameter added in 3.10, `insort` O(n).
- Removed: the `sortedcontainers` suggestion (third party, not in these docs).

Method: documentation only; no commands were run.
