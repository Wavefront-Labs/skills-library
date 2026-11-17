---
id: computing-software.web-development.frontend-development.map-set-weakmap-weakref
name: map-set-weakmap-weakref
category: computing-software
field: web-development
product: frontend-development
tags: [iterators-generators, map-set, weakmap, weakref, set-methods, keyed-collections, javascript]
level: practitioner
status: verified
description: "Choosing Map, Set, WeakMap, WeakSet or WeakRef over plain objects and arrays: key semantics, ordering, new Set methods, GC-friendly caches and serialisation."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WeakMap
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WeakRef
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set/union
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Map, Set, WeakMap, WeakRef

## 1. Choose
| Need | Use |
|---|---|
| Fixed-shape record, JSON | plain object |
| Dictionary with arbitrary/any-type keys, frequent add/delete, size | `Map` |
| Unique values, fast membership | `Set` |
| Attach data to objects you do not own without leaking them | `WeakMap` |
| Mark objects (visited, processed) | `WeakSet` |
| Cache that the GC may drop | `WeakRef` + `FinalizationRegistry` (rarely) |

Objects as dictionaries have traps: `"__proto__"`/`"constructor"` keys, keys coerced to strings (`obj[1] === obj["1"]`), integer-like keys reordered first. `Map` keeps insertion order for all keys and uses SameValueZero (`NaN` equals `NaN`, objects by identity).

## 2. Idioms
```js
const byId = new Map(users.map(u => [u.id, u]));
const counts = new Map(); for (const w of words) counts.set(w, (counts.get(w) ?? 0) + 1);
const unique = [...new Set(ids)];
const groups = Map.groupBy(orders, o => o.status);         // ES2024
const both = a.intersection(b); const onlyA = a.difference(b); // Set methods, Baseline 2024
```

## 3. WeakMap for private/per-object data
```js
const meta = new WeakMap();
function track(el) { meta.set(el, { clicks: 0 }); }   // entry dies when el is GC'd
```
Weak collections are not iterable and have no `size` - by design. Keys must be objects or non-registered symbols (ran: `Symbol('x')` accepted, `Symbol.for('x')` and `1` throw `Invalid value used as weak map key`).

## 4. WeakRef caveats
`deref()` may return `undefined` at any time after the object is unreachable; GC timing is unspecified, and finalizers may never run. Never use for correctness, only for optional caches.

## 5. Serialisation
`JSON.stringify(map)` gives `{}`. Use `Object.fromEntries(map)` (string keys) or `[...map]` entries; revive with `new Map(arr)`. `structuredClone` handles Map/Set directly.

## Verify
Benchmarks are rarely needed - correctness first. Test key semantics: `map.get(NaN)` works; object keys by identity, not equality (two `{id:1}` are different keys).
