---
id: computing-software.web-development.frontend-development.copying-and-freezing-objects
name: copying-and-freezing-objects
category: computing-software
field: web-development
product: frontend-development
tags: [javascript-classes, structuredclone, object-freeze, immutability, deep-copy, javascript]
level: practitioner
status: verified
description: "Copying and freezing objects in JavaScript: spread vs structuredClone vs JSON round-trip, what each loses, Object.freeze depth, and immutable update patterns."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/structuredClone
  - https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Structured_clone_algorithm
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/freeze
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Copying and freezing objects

## 1. Pick the copy
| Method | Depth | Keeps | Loses / throws |
|---|---|---|---|
| `{...o}`, `Object.assign({}, o)`, `[...a]` | shallow | own enumerable props, symbols | prototype (class instances become plain), getters (evaluated) |
| `structuredClone(o)` | deep | Date, Map, Set, RegExp, ArrayBuffer, typed arrays, Error, cycles | functions and DOM nodes throw `DataCloneError`; prototype/class lost; getters evaluated; private fields dropped |
| `JSON.parse(JSON.stringify(o))` | deep | plain data | Date -> string, Map/Set -> `{}`, `undefined`/functions dropped, NaN/Infinity -> null, cycles throw, BigInt throws |

Default: spread for one level, `structuredClone` for deep. Never use JSON round-trip for anything but plain JSON data.

## 2. Immutable updates
```js
const next = { ...state, user: { ...state.user, name: "Ana" } };   // copy along the path only
const items = state.items.map(i => i.id === id ? { ...i, done: true } : i);
const sorted = state.items.toSorted((a, b) => a.n - b.n);            // non-mutating (ES2023)
const without = state.items.toSpliced(idx, 1);
const changed = state.items.with(idx, newItem);
```
For deep nested updates use Immer (`produce`) instead of hand-written spreads.

## 3. Freezing
- `Object.freeze(o)` is **shallow**: nested objects stay mutable. Writes to frozen props fail silently in sloppy mode and throw `TypeError` in strict mode/modules.
- `Object.seal` blocks add/delete but allows writes; `Object.preventExtensions` blocks adds only.
- Deep freeze recursively for config constants:
```js
const deepFreeze = o => { Object.values(o).forEach(v => typeof v === "object" && v !== null && deepFreeze(v)); return Object.freeze(o); };
```
- Freezing does not affect Map/Set internals (`Object.freeze(new Map()).set(1, 2)` still worked, size 1). `Object.freeze` on a typed array with elements throws `TypeError` in Node 20 (elements cannot be frozen), so copy it instead.
- `as const` in TypeScript is compile-time only.

## 4. Pitfalls
- `structuredClone` of a class instance returns a plain object - methods disappear.
- Spread copies of arrays of objects share the objects (mutating `copy[0].x` mutates the original).

Run in Node 20: `structuredClone` kept Date, Map, Set, RegExp, Error, typed arrays and cycles, evaluated an own getter to its value, turned a class instance with a private field and prototype getter into `{ a: 1 }`, and threw `DataCloneError` for functions and symbols; `JSON.stringify` turned Date to ISO text, Map to `{}`, dropped `undefined` and functions, wrote `NaN`/`Infinity` as `null`, and threw `TypeError` for BigInt and cycles. `toSorted`, `toSpliced` and `with` left the source unchanged. In a sloppy-mode CommonJS file a write to a frozen object was silently ignored, in an ES module it threw `TypeError`; a sealed object allowed writes but refused deletes (module/strict `TypeError`).

## Verify
Test: mutate the copy deeply and assert the original is unchanged; in a module, writing to a frozen object throws.
