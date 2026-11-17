---
id: computing-software.software-engineering.python.deque-and-counter
name: deque-and-counter
category: computing-software
field: software-engineering
product: python
tags: [python, py-collections, deque-counter, collections-deque, collections-counter, sliding-window, queue]
level: practitioner
status: docs-checked
description: "Use collections.deque for O(1) queues, sliding windows and rotation, and Counter for frequency tables, top-N and multiset arithmetic."
sources: ["https://docs.python.org/3/library/collections.html#collections.deque", "https://docs.python.org/3/library/collections.html#collections.Counter"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# deque and Counter

## deque
```python
from collections import deque, Counter
q = deque(maxlen=3)            # bounded: appending a 4th evicts from the other end
for x in range(5): q.append(x)  # deque([2, 3, 4], maxlen=3)
q.appendleft(9); q.popleft(); q.rotate(1)
work = deque(tasks)
while work:
    t = work.popleft()          # O(1); list.pop(0) is O(n)
```
- Ends are O(1); indexing the middle is O(n). `deque` is thread-safe for `append`/`popleft` (not a replacement for `queue.Queue` blocking semantics).
- Moving average: keep a `deque(maxlen=k)` plus a running sum.

## Counter
```python
c = Counter("abracadabra")      # Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})
c.most_common(2)                # [('a', 5), ('b', 2)]
c["z"]                          # 0, missing keys return 0 instead of raising
c.update("aaa"); c.subtract("a")
Counter(a=3) + Counter(a=1, b=2)   # addition; subtraction drops zero/negative counts
c1 & c2; c1 | c2                    # min / max per key (multiset intersection/union)
c.total()                           # sum of counts (3.10+)
```

## Gotchas
- `c[k] -= n` can go negative; `+c` strips non-positive entries.
- `Counter` counts hashable items only; count unhashable ones by converting (`tuple(x)`).
- `deque.maxlen` silently discards; if you must not lose items check `len(q) == q.maxlen` before appending.
- Copying a `deque` copies references only.

## Verify
- [ ] Unit test: window of size k yields expected averages at edges (first k-1 elements).
- [ ] `Counter` of a known string matches a hand count; empty input gives an empty Counter.

## Checked

- 2026-11-03: checked against the CPython docs `library/collections.rst`: deque thread-safe O(1) appends/pops, list `pop(0)` O(n), `maxlen` eviction, O(n) middle indexing, `rotate`, Counter zero for missing keys, `total()` new in 3.10, `+c` stripping non-positive counts, `&`/`|` as min/max, shallow `copy()`.
- Removed: the `most_common` versus `heapq.nlargest` remark and the claim that Counter reads do not insert (not stated in the docs).

Method: documentation only; no commands were run.
