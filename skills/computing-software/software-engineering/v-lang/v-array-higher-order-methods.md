---
id: computing-software.software-engineering.v-lang.v-array-higher-order-methods
name: v-array-higher-order-methods
category: computing-software
field: software-engineering
product: v-lang
tags: [v-array-higher-order-methods, arrays, map, filter, any, all, reduce, it, higher-order, arrays module, lambda, v-lang]
level: practitioner
status: docs-checked
description: "Transform arrays with .map, .filter, .any, .all, .count, lambdas and arrays.reduce/sum/min/max using the it variable."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Array map, filter, any, all, reduce

Goal: write declarative array pipelines.

- `doubled := a.map(it * 2)`; `evens := a.filter(it % 2 == 0)`; also with a function literal `a.map(fn (x int) int { return x + 1 })`. `it` is the builtin variable for the element being processed.
- `a.any(it > 3)`, `a.all(it > 0)`, `a.count(it == 2)`.
- Lambda expressions `a.map(|x| x * 10)` and `a.sort(|x, y| x > y)` are valid only inside calls to higher-order functions.
- `import arrays` for: `arrays.sum(a)!`, `arrays.min(a)!`, `arrays.max(a)!` and `arrays.reduce(a, fn (acc int, x int) int { return acc + x })!`; each returns a result and errors on an empty array. Also `arrays.group_by(a, fn)` (returns a map of arrays), `arrays.chunk(a, size)`, `arrays.flatten(a)`, `arrays.map_indexed`, `arrays.filter_indexed`, `arrays.fold`.
- Chain calls: `files.filter(it#[-4..].to_lower() == '.jpg').map(it.to_upper())`.

Gotchas:
- `arrays.sum`, `min`, `max` and `reduce` return `!T`, so handle the error with `!` or `or`.

Verify: `assert [1, 2, 3].map(it * 2) == [2, 4, 6]`.

## Checked

Date: 2026-11-03. Confirmed in the V documentation (doc/docs.md, "Array methods", "Array method chaining", "Lambda expressions") and vlib/arrays/arrays.v and vlib/builtin/array.v (signatures of `sum`, `min`, `max`, `reduce`, `group_by`, `chunk`, `flatten`, `map_indexed`, `filter_indexed`, `fold`, `count`). Removed: `arrays.zip` (no such function in arrays.v), `a.map(square)` with a bare function name, the `a.map(it)` index note, and the nested-`it` shadowing remark.

Method: documentation only; no commands were run.
