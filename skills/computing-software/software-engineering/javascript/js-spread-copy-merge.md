---
id: computing-software.software-engineering.javascript.js-spread-copy-merge
name: js-spread-copy-merge
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, spread-merge, js-destructuring]
level: practitioner
status: docs-checked
description: "Copy and merge arrays and objects with spread: shallow copies, override order, conditional members, and how spread differs from Object.assign."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spread for copying and merging

- Spread works in function argument lists, array literals and object literals. Only iterables (Array, String) spread in array literals and argument lists; a plain object there throws `TypeError: obj is not iterable`.
- In object literals, spread enumerates own properties. Arrays spread into objects by index (`{ ...[1, 2, 3] }` is `{ 0: 1, 1: 2, 2: 3 }`). All primitives can be spread into objects, but only strings produce properties.
- `{ ...obj1, ...obj2 }` merges; on duplicate names the property takes the last value while keeping its original position (`{ x: 41, ...obj1, ...obj2, y: 9 }` gives `{ x: 42, foo: "baz", y: 9 }` in the MDN example).
- A single spread is a shallow copy, without non-enumerable properties and without the prototype. `[...arr]` is like `arr.slice()`. Copying goes one level deep, so nested arrays/objects stay shared; no native operation deep-clones, and `structuredClone()` deep-copies supported types.
- Conditional members: `...(isSummer ? ["watermelon"] : [])` adds nothing when false, unlike `isSummer ? "watermelon" : undefined`, which adds an `undefined` element. For objects `...(isSummer && { watermelon: 30 })` works because falsy values have no enumerable properties.
- `Object.assign()` mutates its target and triggers setters; spread does not. Replace it with `objects.reduce((acc, cur) => ({ ...acc, ...cur }))`; `({ ...objects })` on a rest array wrongly spreads the array.
- `[...arr1, ...arr2]` replaces `concat`/`unshift.apply` and creates a new array rather than modifying one in place.
- Spreading very large arrays in a call can exceed the engine's argument length limit (see `Function.prototype.apply()`).

Self-check: mutate a nested field of a spread copy and confirm the original changed.

## Checked

Confirmed against MDN "Spread syntax (...)" (page last modified 2026-05-22), read 2026-11-08. Removed: the claim about spreading `null`/`undefined`, symbol keys, destructuring-based key removal and the "stack overflow" wording (the page says argument length limit).
Method: docs-only read of cited pages, 2026-11-08
