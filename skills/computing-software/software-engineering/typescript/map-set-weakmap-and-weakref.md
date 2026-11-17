---
id: computing-software.software-engineering.typescript.map-set-weakmap-and-weakref
name: map-set-weakmap-and-weakref
category: computing-software
field: software-engineering
product: typescript
tags: [javascript, js-map-set, weakmap, weakref, finalizationregistry, set-methods, collections]
level: practitioner
status: docs-checked
description: "Choose JavaScript keyed collections: Map vs object dictionaries, Set and its ES2025 methods, WeakMap/WeakSet for metadata without leaks, and when WeakRef is appropriate."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map/groupBy
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WeakMap
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WeakRef
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set/union
  - https://github.com/mdn/browser-compat-data/blob/main/javascript/builtins/Set.json
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Map, Set, WeakMap and WeakRef

**Goal:** the right container for dynamic keys, membership tests and per-object
metadata, without memory leaks.

## Map vs plain object
```js
const byId = new Map();             // any key type, insertion-ordered, .size, fast add/delete
byId.set(user.id, user);
byId.get("u1"); byId.has("u1"); byId.delete("u1");
for (const [id, u] of byId) { ... }
const grouped = Map.groupBy(orders, (o) => o.status);      // Node 21+
```
Plain objects as dictionaries have traps: inherited keys (`"constructor" in {}` is true),
`__proto__` key behaviour, string-only keys (`obj[1]` and `obj["1"]` collide), no size. Use
`Map` for dynamic keys; objects for fixed-shape records and JSON. `Object.create(null)` if you
must use an object dictionary.

JSON: `JSON.stringify(map)` gives `{}`; convert with `Object.fromEntries(map)` /
`new Map(Object.entries(obj))`.

## Set
```js
const seen = new Set(ids);              // dedupe: [...new Set(arr)]
seen.has(x);                            // O(1) vs array.includes O(n)
a.union(b); a.intersection(b); a.difference(b); a.isSubsetOf(b);   // Set methods, Node 22+
```
Equality is SameValueZero: objects compare by reference; `NaN` equals `NaN`.

## WeakMap / WeakSet: metadata without leaks
```js
const cache = new WeakMap();            // keys must be objects (or non-registered symbols)
function layout(el) {
  if (!cache.has(el)) cache.set(el, expensiveMeasure(el));
  return cache.get(el);
}
```
Entries disappear when the key object is garbage collected. Not iterable, no `size` - by
design. Classic uses: caching derived data per DOM node/request object, private data for
objects you don't own, marking visited objects (WeakSet).

A regular `Map` keyed by objects keeps them alive forever -> the common "cache leak".

## WeakRef and FinalizationRegistry
```js
const ref = new WeakRef(bigObject);
const obj = ref.deref();               // undefined once collected
const registry = new FinalizationRegistry((key) => cache.delete(key));
```
GC timing is unspecified; callbacks may run late or never. Use only for caches of
re-creatable objects, never for correctness (closing files, releasing locks - use
`try/finally` or `using` declarations instead).

## Verify
- [ ] Caches keyed by objects use WeakMap or have explicit eviction.
- [ ] No object-literal dictionaries fed by user-controlled keys.

## Checked
Checked 2026-10-25 against the MDN content repository and MDN browser-compat-data (Map.json, Set.json). Confirmed: WeakMap keys must be objects or non-registered symbols and WeakMap is not enumerable; WeakRef and FinalizationRegistry timing is implementation-defined and best avoided; Map.groupBy ships in Node 21 and the Set methods (union, intersection, difference, isSubsetOf) in Node 22. Replaced spec-year labels with the Node versions from the compatibility data.
Method: documentation only; no commands were run.
