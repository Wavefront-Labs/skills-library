---
id: computing-software.software-engineering.v-lang.v-arrays-module-helpers
name: v-arrays-module-helpers
category: computing-software
field: software-engineering
product: v-lang
tags: [v-arrays-module-helpers, arrays-math-strconv, arrays module, arrays.sum, arrays.min, chunk, window, flatten, group_by, zip, binary_search, concat, v-lang]
level: practitioner
status: docs-checked
description: "Use arrays.sum, min, max, reduce, chunk, window, flatten, group_by, zip and binary_search for common array algorithms."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The arrays module

Goal: avoid hand-written loops for common array work.

- `import arrays`.
- Aggregates: `arrays.sum(a)!`, `arrays.min(a)!`, `arrays.max(a)!`, `arrays.reduce(a, fn (acc int, x int) int { return acc + x })!`.
- Shape: `arrays.chunk(a, 3)`, `arrays.window(a, size: 3, step: 1)`, `arrays.flatten(nested)`, `arrays.concat(a, ...b)`, `arrays.merge(a, b)` (merges two ascending sorted arrays).
- Grouping: `arrays.group_by(a, fn (x V) K { ... })` returns `map[K][]V`; `arrays.partition(a, predicate)` returns two arrays.
- Fold and iterate: `arrays.fold(a, init, fn (acc R, x T) R { ... })`, `arrays.each(a, fn (x T) { ... })`.
- Search: `arrays.binary_search(a, v)!` on sorted data, `arrays.find_first(a, predicate)` and `arrays.find_last(a, predicate)` (both return an option).

Gotchas:
- Many return results because empty input is undefined.

Verify: `assert arrays.sum([1,2,3])! == 6`.

## Checked

2026-11-03. Confirmed against the V repository source (vlib modules and doc/docs.md) read in this batch: signatures and doc comments of sum, min, max, reduce, chunk, window (WindowAttribute size/step), flatten, concat, merge, group_by, partition, fold, each, binary_search, find_first, find_last (vlib/arrays/arrays.v).
Removed or corrected: `arrays.zip` (no such function in vlib/arrays), the '(confirm)' markers, and the 'function names evolve' note.
Method: documentation only; no commands were run.
