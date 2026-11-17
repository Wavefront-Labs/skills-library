---
id: computing-software.software-engineering.javascript.js-array-methods-and-sorting
name: js-array-methods-and-sorting
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-arrays, array-methods, array-sort, array-groupby]
level: practitioner
status: docs-checked
description: "Choose the right Array method and avoid mutation, sort and sparse-array pitfalls."
sources: ["https://tc39.es/ecma262/", "https://developer.mozilla.org/en-US/docs/Web/JavaScript"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Array methods

- Transform: `map`, `filter`, `flatMap`, `reduce` (always pass an initial value), `find/findLast/findIndex`, `some/every`, `includes` (handles NaN, `indexOf` does not), `at(-1)`, `Array.from({ length: n }, fn)`.
- Mutating: `push/pop/shift/unshift/splice/sort/reverse/fill/copyWithin`. Non-mutating copies (ES2023): `toSorted`, `toReversed`, `toSpliced`, `with`.
- Default `sort()` compares as strings: `[10, 9, 1].sort()` gives `[1, 10, 9]`. Pass a comparator `(a, b) => a - b`. `sort` is stable (guaranteed by the spec since ECMAScript 2019). Comparators must be consistent and return a number, not a boolean.
- Grouping: `Object.groupBy(arr, fn)` / `Map.groupBy` (ES2024) where supported.
- `forEach` ignores `await` (does not wait); use `for...of` with await or `Promise.all(arr.map(...))`.
- Holes in sparse arrays are skipped by `forEach` (callbacks run only for assigned indexes); avoid `new Array(n)` then `map`; use `Array.from`.
- `delete arr[i]` leaves a hole; use `splice`.
- `arr.length = 0` clears in place.

## Checked

2026-11-02. Checked against MDN Array, Array.prototype.sort, toSorted, Object.groupBy and Array.prototype.forEach (default string sort, stable sort since ES2019, comparator rules, non-mutating toSorted family, Object.groupBy / Map.groupBy, forEach does not wait for promises, forEach skips empty slots). Removed: the claim about which iteration forms visit holes beyond forEach.

Method: documentation only; no commands were run.
