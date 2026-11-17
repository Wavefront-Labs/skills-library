---
id: computing-software.software-engineering.javascript.js-set-operations
name: js-set-operations
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, set-methods, js-collections]
level: practitioner
status: docs-checked
description: "Use Set composition methods (union, intersection, difference) and their filter fallbacks; know Set equality rules."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Set algebra patterns

- Set composition methods: `a.union(b)`, `intersection`, `difference`, `symmetricDifference` return a new `Set`; `isSubsetOf`, `isSupersetOf`, `isDisjointFrom` return booleans. Check browser compatibility before relying on them.
- The argument only needs to be set-like (a numeric `size`, a `has()` method and a `keys()` method returning an iterator), so a `Map` works (its keys are used) but an array or `WeakSet` does not; `this` must be a real `Set`.
- Fallbacks from MDN: intersection `new Set([...a].filter((x) => b.has(x)))`, difference `new Set([...a].filter((x) => !b.has(x)))`.
- Sets keep insertion order and compare with SameValueZero: `NaN` equals `NaN`, and objects compare by reference, not value.
- Dedupe an array with `[...new Set(arr)]`; `forEach` and `for...of` iterate in insertion order.

Self-check: `new Set([NaN, NaN]).size` is 1.

## Checked

Date: 2026-11-03. Confirmed on MDN Global_Objects/Set: composition methods and return types, set-like requirements, fallback filter examples, SameValueZero and reference equality, insertion order, dedupe example. Removed as not covered by the Set page: Map insertion order and SameValueZero claims, `new Map(Object.entries(o))`, `Object.fromEntries(map)`, the Map forEach argument order, and `JSON.stringify(map)`; the "ES2025" label (the page only says to check compatibility).

Method: documentation only; no commands were run.
