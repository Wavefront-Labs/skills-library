---
id: computing-software.software-engineering.javascript.js-array-flat-reduce-group
name: js-array-flat-reduce-group
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, array-flatmap, js-arrays]
level: practitioner
status: docs-checked
description: "Use Array.prototype.flatMap to map and flatten one level; know sparse-array behaviour."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/flatMap"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# flatMap

- `arr.flatMap(fn)` returns a new array formed by applying the callback to each element and then flattening the result by one level (depth 1). It is identical to `arr.map(fn).flat()` but slightly more efficient.
- Only one level is flattened: nested arrays deeper than the returned level stay nested.
- On sparse arrays the callback is not called for empty slots (as with `map()`), and `flat()` ignores empty slots in the returned arrays.
- The callback also receives the array as its third argument, e.g. to look at other elements.

Self-check: `[1, 2].flatMap((x) => [x, x * 2])` returns `[1, 2, 2, 4]`.

## Checked

Date: 2026-11-03. Confirmed on MDN Array/flatMap: one-level flattening, equivalence to map then flat, sparse behaviour, array argument. Removed as not on that page: `flat(depth)` and `Infinity`, reduce initial-value advice, Object.groupBy and Map.groupBy, Set dedupe, the Map-by-id idiom, Array.from ranges, `new Array(3)` holes; the title and description no longer promise them.

Method: documentation only; no commands were run.
