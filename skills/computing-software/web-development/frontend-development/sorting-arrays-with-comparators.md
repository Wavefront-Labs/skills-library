---
id: computing-software.web-development.frontend-development.sorting-arrays-with-comparators
name: sorting-arrays-with-comparators
category: computing-software
field: web-development
product: frontend-development
tags: [array-sort-comparator, stable-sort, localecompare, tosorted, multi-key-sort, javascript]
level: practitioner
status: verified
description: "Correct array sorting in JavaScript: comparator contracts, default string sort trap, stable multi-key sorts, toSorted, and locale-aware string order with Intl.Collator."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Collator
  - https://v8.dev/features/stable-sort
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sorting with comparators

## 1. The default sort is a string sort
```js
[10, 9, 1, 100].sort();          // [1, 10, 100, 9]
[10, 9, 1, 100].sort((a, b) => a - b);   // [1, 9, 10, 100]
```
`sort()` mutates and returns the same array; `toSorted()` (Baseline 2023) returns a copy, which is what React state needs.

## 2. Comparator contract
Return negative / zero / positive, and be **consistent** (same inputs, same answer; transitive). Returning booleans (`a > b`) is wrong: `false` and `true` coerce to 0/1, never negative, giving engine-dependent order (in Node 20 `[5,1,4,2,3,...].sort((a, b) => a > b)` left the array in its original order). A comparator that can return `NaN` (missing fields) corrupts the result.
`undefined` elements are moved to the end without calling the comparator; holes after that.

## 3. Strings
```js
const coll = new Intl.Collator(undefined, { numeric: true, sensitivity: "base" });
files.sort((a, b) => coll.compare(a.name, b.name));   // "file2" < "file10", "a" == "A"
```
Reuse one Collator: `a.localeCompare(b, ...)` with options is slow on big arrays (3.4 s vs 0.1 s for 50 000 strings in Node 20). Plain `<` compares UTF-16 code units: "Z" < "a", "é" after "z".

## 4. Multi-key and stable sorts
Sort is stable (ES2019): equal elements keep input order (checked: 30 items with key `i % 3` kept index order within each key). Multi-key in one pass:
```js
rows.toSorted((a, b) =>
  a.lastName.localeCompare(b.lastName) ||
  b.createdAt - a.createdAt ||           // Dates subtract to ms; newest first
  a.id - b.id);
```

## 5. Expensive keys
Precompute (decorate-sort-undecorate) when the key is costly:
```js
rows.map(r => [key(r), r]).sort((x, y) => x[0] - y[0]).map(([, r]) => r);
```

## Gotchas
- Sorting date strings works only for ISO-8601 with the same offset; parse otherwise.
- `null` values: decide explicitly (`(a.v ?? Infinity) - (b.v ?? Infinity)`).
- Sorting server-paginated data client-side sorts only the current page.

## Verify
- [ ] Test with numbers > 9, mixed case, accented names, null fields and equal keys.
