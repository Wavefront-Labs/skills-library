---
id: computing-software.software-engineering.javascript.js-array-immutable-methods
name: js-array-immutable-methods
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, array-tosorted, js-arrays]
level: practitioner
status: docs-checked
description: "Use Array.prototype.toSorted for a sorted copy; know the default sort comparison and sparse-array behaviour."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/toSorted"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Non-mutating sort

- `toSorted(compareFn)` returns a new array sorted ascending; the original is unchanged (`months.toSorted()` leaves `months` as it was).
- Without `compareFn`, elements are converted to strings and sorted by Unicode code point, so numbers need a comparator: `values.toSorted((a, b) => a - b)` gives `[1, 2, 10, 21]` for `[1, 10, 21, 2]`.
- On sparse arrays, empty slots are treated as `undefined` and sorted to the end; `compareFn` is not called for them.
- It is generic: it only needs `length` and integer-keyed properties.
- Check browser and runtime support before relying on it; see MDN's compatibility table.

Self-check: after `const b = a.toSorted()`, `a` is unchanged.

## Checked

Date: 2026-11-03. Confirmed on MDN Array/toSorted: return value, default string comparison, comparator example, sparse handling, generic. Removed as not stated there: toReversed/toSpliced/with/at/findLast, the Node version, the React state remark, and the specific `[10, 9, 1].sort()` result.

Method: documentation only; no commands were run.
