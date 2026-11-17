---
id: computing-software.software-engineering.v-lang.v-array-sorting-and-searching
name: v-array-sorting-and-searching
category: computing-software
field: software-engineering
product: v-lang
tags: [v-array-sorting-and-searching, arrays, sort, sorted, sort_with_compare, reverse, binary search, index, comparator, v-lang]
level: practitioner
status: docs-checked
description: "Sort with .sort and .sorted using a and b comparators, sort_with_compare, reverse, index and binary search."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sorting, searching and reversing arrays

Goal: order and look up data.

- In place: `a.sort()` ascending, `a.sort(a > b)` descending (the special variables `a` and `b` are the compared elements), `a.sort(a.name < b.name)` for struct fields.
- Copy: `s := a.sorted()`, `a.sorted(b < a)`; `sorted_with_compare` is the copying form of `sort_with_compare`.
- Function comparator: `a.sort_with_compare(fn (x &Item, y &Item) int { ... })`; return -1 when the first comes before the second, 0 when equal, 1 otherwise.
- Reverse: `a.reverse()` makes a new array; `a.reverse_in_place()` modifies it.
- Search: `a.index(v)` returns the first position or -1 (`last_index` for the last); `a.contains(v)`; `v in a`. `arrays.binary_search(a, v)!` requires sorted input and returns the index or an error.
- `a.first()`, `a.last()`.

Gotchas:
- In-place `.sort` needs `mut a`.
- `sort` and `sorted` keep equal elements in their original relative order (stable per vlib/builtin/array.v).
- Float NaNs sort last with no argument.

Verify: `assert [3, 1, 2].sorted() == [1, 2, 3]`.

## Checked

Date: 2026-11-03. Confirmed in the V documentation (doc/docs.md, "Sorting Arrays", "Array methods") and vlib/builtin/array.v, vlib/arrays/arrays.v (doc comments for `sort`, `sorted`, `sort_with_compare`, `index`, `last_index`, `contains`, `binary_search`). Removed: the "sorting is not guaranteed stable" caveat (the source says equal elements keep their order).

Method: documentation only; no commands were run.
