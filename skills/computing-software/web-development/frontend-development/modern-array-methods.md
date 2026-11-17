---
id: computing-software.web-development.frontend-development.modern-array-methods
name: modern-array-methods
category: computing-software
field: web-development
product: frontend-development
tags: [iterators-generators, array-methods, object-groupby, javascript, es2023]
level: practitioner
status: docs-checked
description: "Using modern array methods: at, findLast, toSorted/toReversed/with, flatMap, Object.groupBy, Array.from with mappers, and avoiding mutation and sort pitfalls."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/toSorted
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/groupBy
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/fromAsync
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort
  - https://github.com/mdn/browser-compat-data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Modern array methods

## 1. Non-mutating replacements (ES2023, Baseline 2023)
| Mutates | Copy version |
|---|---|
| `sort()` | `toSorted()` |
| `reverse()` | `toReversed()` |
| `splice()` | `toSpliced()` |
| `arr[i] = v` | `with(i, v)` |
Use these on state (React/Redux) and on arrays you received as arguments.

## 2. Lookup
- `at(-1)` last element; typed arrays have their own `at()`.
- `findLast` / `findLastIndex` search from the end.
- `includes(NaN)` is true; `indexOf(NaN)` is -1.

## 3. Grouping and building
```js
const byStatus = Object.groupBy(orders, o => o.status);  // null-prototype object of arrays
const byUser = Map.groupBy(orders, o => o.user);         // object keys
const range = Array.from({ length: 5 }, (_, i) => i * 2); // [0,2,4,6,8]
const tags = posts.flatMap(p => p.tags);
const fromAsync = await Array.fromAsync(asyncIterable);   // Baseline 2024
```
`Object.groupBy` returns an object without a prototype - `result.hasOwnProperty` is undefined; use `Object.hasOwn`.

## 4. Sort correctly
- Default `sort()` compares strings: `[10, 9, 1].sort()` gives `[1, 10, 9]`. Numbers: `(a, b) => a - b`.
- Locale text: `arr.toSorted(new Intl.Collator("de").compare)`.
- Sort is stable since ES2019 - chain secondary keys by sorting in multiple passes or with `||` in the comparator.

## 5. Pitfalls
- `forEach` ignores `await` - use `for...of` for sequential async, `Promise.all(arr.map(...))` for parallel.
- `map(parseInt)` passes the index as radix: `["1","2","3"].map(parseInt)` -> `[1, NaN, NaN]`. Use `map(Number)`.
- `reduce` without initial value throws on empty arrays.
- Sparse arrays (`new Array(3)`) skip holes in `map`/`forEach`.
- `Array(3).fill({})` shares one object across all slots.

## Verify
Check target support (Browserslist/caniuse) or polyfill with core-js for `toSorted`/`groupBy` if you support Safari < 16/17.

## Checked

2026-10-26. MDN pages for toSorted, Object.groupBy (null-prototype result), Array.sort (default string comparison; stable since ES2019), includes (SameValueZero), reduce (no initial value throws TypeError on an empty array), fill (shared object reference), forEach (does not wait for promises) and browser-compat-data: toSorted/with/toSpliced Chrome 110, Firefox 115, Safari 16; groupBy Chrome 117, Firefox 119, Safari 17.4; Array.fromAsync Chrome 121, Firefox 115, Safari 16.4. The core-js pointer was left as a generic polyfill suggestion.

Method: documentation only; no commands were run.
