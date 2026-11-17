---
id: computing-software.software-engineering.concurrency.algorithmic-complexity-first
name: algorithmic-complexity-first
category: computing-software
field: software-engineering
product: concurrency
tags: [concurrency, optimisation, algorithmic-complexity, big-o, data-structures, n-plus-one, scalability]
level: practitioner
status: gated
description: "Get the big performance wins first by fixing algorithmic complexity: spotting accidental O(n^2), choosing data structures, N+1 queries, and verifying with scaling benchmarks."
sources:
  - https://www.bigocheatsheet.com/
  - https://accidentallyquadratic.tumblr.com/
  - https://docs.python.org/3/library/collections.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Algorithmic complexity wins first

Micro-optimisations give percentages; complexity changes give orders of magnitude. Before tuning code paths, check what the code does as n grows.

## Spot accidental quadratic behaviour
| Pattern | Cost | Fix |
|---|---|---|
| `if x in some_list` inside a loop | O(n x m) | build a `set`/`dict`/`HashSet` once: O(n + m) |
| `list.remove(x)` / `list.pop(0)` / `insert(0, x)` in a loop | O(n^2) | `collections.deque`, mark-and-compact, or build a new list |
| String concatenation in a loop (`s += piece`) in Go (measured 5.9, 30, 93, 405 ms for 2k-16k pieces) and Python 3.14 on Windows (about 4.6x per doubling); Java/C# not run (gated: unconfirmed, source is paywalled or blocked) | O(n^2) copying | `StringBuilder`, `strings.Builder`, `"".join(parts)` |
| Nested loop to join two collections | O(n x m) | index one side by key (hash join) |
| Sorting inside a loop | O(n^2 log n) | sort once, or use a heap (`heapq`, `PriorityQueue`) |
| Repeated `array.indexOf`/`find` in JS loops | O(n^2) | `Map`/`Set` |
| Recomputing aggregates on every step | O(n^2) | running totals, prefix sums |
| Regex with nested quantifiers on user input | exponential (ReDoS) | rewrite pattern, use RE2/linear engines |
| Recursive Fibonacci-style overlapping subproblems | exponential | memoise (`functools.cache`) / dynamic programming |
See accidentallyquadratic.tumblr.com for real-world cases.

## Distributed version: N+1 and chatty calls
- ORM lazy loading in a loop issues one query per row: use eager loading (`select_related`/`prefetch_related`, JPA `JOIN FETCH`/entity graphs, EF Core `Include` (gated: unconfirmed, source is paywalled or blocked), GraphQL DataLoader batching).
- One HTTP call per item: batch endpoints or bulk queries (`WHERE id IN (...)` / `= ANY($1)`).
- Detect: query counts per request in logs/APM, `nplusone` (Python), Hibernate statistics (gated: unconfirmed, source is paywalled or blocked), Bullet (Rails), `django-debug-toolbar`, test assertions on query count (`assertNumQueries`).

## Choose the right data structure
- Membership/lookup: hash set/map O(1) average; sorted order needed: balanced tree (`TreeMap`, `SortedDict`) O(log n) or sort + binary search (`bisect`).
- Top-k: heap O(n log k) instead of full sort.
- Range queries: sorted arrays, interval trees, DB indexes.
- Know your language's hidden costs (Python: `list` slicing copies, `len` is O(1), `in` on list is O(n); Java `LinkedList.get(i)` is O(n) (gated: unconfirmed, source is paywalled or blocked)).

## Verify with scaling benchmarks
Time the operation at n, 2n, 4n, 8n. Linear doubles; quadratic quadruples. A single benchmark at one size hides complexity problems.
Measured (Python 3.14, Node 20, time ratio per doubling of n): `x in list` in a loop 4.0x (8000 items: 559 ms) versus `in set` 2.0x; `list.pop(0)` 4.0x versus `deque.popleft()` 2.0x; `heapq.nlargest(10, d)` 3.4 ms versus `sorted(d)[-10:]` 30 ms for 200k floats; Node `indexOf` loop over 40k items 1300 ms versus `Set.has` 0.7 ms; `re.match(r'(a+)+$', 'a'*n+'b')` about 4x per +2 characters in Python (16 to 22 characters: 2 to 169 ms) and `(a+)+$` in V8 hit 2.4 s at 28 characters, while Go `regexp` took 5.5 ms for 80,000 characters (linear time); `big[:]` copies a 1M-item list (7 ms) while `len()` is a constant 39 ns.
```python
for n in (1_000, 2_000, 4_000, 8_000):
    data = make_input(n)
    t = timeit.timeit(lambda: process(data), number=5) / 5
    print(n, f"{t*1000:.1f} ms")
```
Profile first to find where time goes; then ask whether the hot function's complexity is the problem before shaving constants.

## Verify
- [ ] Scaling benchmark shows the expected growth after the change.
- [ ] Regression test with a production-sized input runs within a time budget (or query-count assertion for N+1).
