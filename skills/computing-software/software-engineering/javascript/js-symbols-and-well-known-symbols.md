---
id: computing-software.software-engineering.javascript.js-symbols-and-well-known-symbols
name: js-symbols-and-well-known-symbols
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-symbols, symbol-iterator, symbol-toprimitive, symbol-for]
level: practitioner
status: docs-checked
description: "Use Symbol for unique keys and the well-known symbols (iterator, hasInstance, toStringTag, species) as language protocols."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Symbols

- `Symbol("desc")` creates a unique primitive; `Symbol.for("key")` reads or creates a symbol in the global registry (usable across files and realms) and `Symbol.keyFor` reverses it.
- Symbol-keyed properties are skipped by `for...in` and `JSON.stringify`; list them with `Object.getOwnPropertySymbols()`.
- Well-known symbols are static properties of `Symbol` that act as protocols for built-in operations, with the same values across realms: `Symbol.iterator` (`for...of`), `Symbol.asyncIterator` (`for await...of`), `Symbol.hasInstance` (`instanceof`), `Symbol.toStringTag` (`Object.prototype.toString()`), `Symbol.toPrimitive` (conversion to a primitive), `Symbol.species` (constructor for derived objects), `Symbol.isConcatSpreadable` (`concat()`).
- Use symbols for collision-free property keys; they give only weak encapsulation. For real privacy use `#private` fields.
- A symbol cannot be implicitly converted to a string: `Symbol("foo") + "bar"` throws `TypeError`. `String(sym)` and `sym.toString()` work, and `sym.description` is the read-only description.

## Checked

Date: 2026-11-03. Confirmed on MDN Global_Objects/Symbol: registry behaviour, for...in and JSON.stringify skipping, getOwnPropertySymbols, the well-known symbol list and what each is used by, weak encapsulation, conversion rules, description. Removed as not stated there: Object.keys, Reflect.ownKeys, the toPrimitive hint values, "reach them via reflection".

Method: documentation only; no commands were run.
