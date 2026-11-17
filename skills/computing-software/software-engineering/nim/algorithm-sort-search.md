---
id: computing-software.software-engineering.nim.algorithm-sort-search
name: algorithm-sort-search
category: computing-software
field: software-engineering
product: nim
tags: [algorithm-sort-search, stdlib-sequtils-algorithm, algorithm, sort, sorted, binarysearch, reverse, nextpermutation, cmp, sortedbyit, nim]
level: practitioner
status: docs-checked
description: "Sort with custom comparators and key functions, binary search, reverse, rotate and generate permutations."
sources:
  - https://nim-lang.org/docs/algorithm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# algorithm: sort, binarySearch and permutations

Goal: order and search data.

- `import std/algorithm`. `s.sort()` in place, `sorted(s)` copy; `s.sort(proc(a,b: T): int = cmp(a.age, b.age))`, `order = Descending`.
- Key helper: `s.sortedByIt(it.name)` (a template in `std/algorithm`), tuple keys `(it.a, it.b)` for multi-key sorts.
- `cmp(a, b)` returns -1/0/1; default `<` ordering works for ints, strings, tuples.
- Search sorted data: `binarySearch(s, x)` returns index or -1; `lowerBound`, `upperBound`.
- Others: `reverse`, `reversed`, `rotateLeft`, `nextPermutation`, `isSorted`, `fill`, `product`.
- `sort` is the default Nim sort, a merge sort: guaranteed stable, worst case O(n log n).
- `binarySearch` returns the index of the key, or -1 if not found.

Gotchas:
- To use the default `sort` on a custom type you need `cmp`/`<` defined for it.

Verify: `sorted(@[3,1,2])` is @[1,2,3].

## Checked

2026-11-02. Confirmed against lib/pure/algorithm.nim (all listed procs exist; stable merge sort doc; `binarySearch` returns -1). Fixed: `sortedByIt` lives in `std/algorithm`. Removed: the strict-weak-ordering claim.
Method: documentation only; no commands were run.
