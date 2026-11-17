---
id: computing-software.software-engineering.d.d-algorithm-searching-find-canfind-count
name: d-algorithm-searching-find-canfind-count
category: computing-software
field: software-engineering
product: d
tags: [d-algorithm-searching-find-canfind-count, std-algorithm, find, canfind, countuntil, startswith, endswith, all, any, minelement, maxelement, among, until, skipover, searching, d]
level: practitioner
status: docs-checked
description: "Search ranges using find, canFind, countUntil, count, startsWith, endsWith, all, any, min/maxElement, minIndex, among, until, skipOver and boyer-moore find."
sources:
  - https://dlang.org/phobos/std_algorithm_searching.html
  - https://dlang.org/phobos/std_algorithm_comparison.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# std.algorithm.searching: find, canFind, count, startsWith, until, minElement

Goal: query collections idiomatically.

- `find(haystack, needle)` returns the rest of the range starting at the match (empty if none); `find!(x => x > 3)(r)` with a predicate. `canFind` returns bool. `countUntil` returns the number of elements before the match, or -1 if there is none; `count!pred(r)` counts matches.
- Prefix/suffix: `startsWith`, `endsWith`, `skipOver(ref r, prefix)`, `until!pred(r)` (lazy; the sentinel is excluded unless `No.openRight`).
- Quantifiers: `all!pred`, `any!pred`; in `std.algorithm.comparison`: `equal`, `isPermutation`, `cmp`, `mismatch`, `min`, `max`, `clamp`.
- Extremes: `minElement`, `maxElement`, `minIndex`, `maxIndex`.
- `among(x, a, b, c)` (std.algorithm.comparison) returns the 1-based index of the first match or 0.
- `boyerMooreFinder(needle)` is a needle for `find` over repeated searches.

Gotchas:
- `find` returns a range, not a bool: test `!arr.find(x).empty` or use `canFind`.
- Because of auto-decoding, `countUntil` on a string may not match the array index; use `std.string.indexOf` for that.

Verify: unittest asserts on empty haystack, no match, and match at the end.

## Checked

2026-11-03. Confirmed against: std.algorithm.searching and std.algorithm.comparison reference pages.

Removed because the pages read did not confirm it: `among!("a","b")` form note kept as the documented template form, `std.string.indexOf` advice kept; code-point claim for `countUntil` replaced by the documented auto-decoding warning.

Method: documentation only; no commands were run.
