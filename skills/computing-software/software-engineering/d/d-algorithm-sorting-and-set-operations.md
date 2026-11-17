---
id: computing-software.software-engineering.d.d-algorithm-sorting-and-set-operations
name: d-algorithm-sorting-and-set-operations
category: computing-software
field: software-engineering
product: d
tags: [d-algorithm-sorting-and-set-operations, std-algorithm, sort, schwartzsort, partialsort, topn, sortedrange, lowerbound, setunion, setintersection, remove, copy, reverse, mutation, d]
level: practitioner
status: docs-checked
description: "Sort with sort/schwartzSort/partialSort/topN, binary search with sortedRange.contains/lowerBound, setUnion/setIntersection, copy, remove, swap, reverse, fill."
sources:
  - https://dlang.org/phobos/std_algorithm_sorting.html
  - https://dlang.org/phobos/std_algorithm_mutation.html
  - https://dlang.org/phobos/std_algorithm_setops.html
  - https://dlang.org/phobos/std_range.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# std.algorithm sorting, mutation and set operations

Goal: sort, search sorted data, and mutate in place.

- `sort(arr)`, `sort!((a, b) => a.k < b.k)(arr)`; the default `SwapStrategy` is unstable, `sort!(less, SwapStrategy.stable)` is stable. The result is a `SortedRange`, so `.contains(x)`, `.lowerBound(x)`, `.upperBound(x)`, `.equalRange(x)` apply. Also `assumeSorted`, `isSorted`, `merge`.
- Other sorting: `schwartzSort!(x => x.name)(arr)` caches the key; `multiSort!("a.x < b.x", "a.y > b.y")(arr)`; `partialSort(arr, k)`, `topN(arr, k)`, `nextPermutation`.
- Mutation (`std.algorithm.mutation`): `copy`, `fill`, `reverse`, `swap`, `swapAt`, `move`, `remove` (default `SwapStrategy.stable`; `remove!(SwapStrategy.unstable)` is the cheaper variant that does not keep order), `bringToFront`, `strip`, `stripLeft`, `uninitializedFill`.
- Set operations on sorted ranges: `setIntersection`, `setDifference`, `setSymmetricDifference`, `multiwayUnion`, `multiwayMerge`.

Gotchas:
- `remove` returns the shortened range and does not shrink the original array variable: assign `a = a.remove(1);`.

Verify: unittest sorts random data and `assert(isSorted(data))`.

## Checked

2026-11-03. Confirmed against: std.algorithm.sorting, std.algorithm.mutation, std.algorithm.setops and std.range reference pages.

Removed because the pages read did not confirm it: `setUnion` (not in the setops page; replaced by `multiwayUnion`), the claim that `sort` on `string` decodes, the expensive-struct sorting advice.

Method: documentation only; no commands were run.
