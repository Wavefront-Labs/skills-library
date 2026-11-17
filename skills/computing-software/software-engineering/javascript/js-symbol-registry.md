---
id: computing-software.software-engineering.javascript.js-symbol-registry
name: js-symbol-registry
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, symbol-for, js-symbols]
level: practitioner
status: docs-checked
description: "Use Symbol.for and Symbol.keyFor for shared symbols; know symbol property key and conversion behaviour."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Global symbol registry and symbol keys

- Every `Symbol("x")` call returns a unique symbol, even with the same description; `Symbol.for("key")` returns the same symbol for the same key, across files and realms, via the global symbol registry.
- `Symbol.keyFor(sym)` is the inverse of `Symbol.for`: `Symbol.keyFor(Symbol.for("tokenString")) === "tokenString"`.
- Registered symbols behave almost exactly like the strings they wrap: they are not guaranteed unique and are not garbage collectable, so they are disallowed in `WeakMap`, `WeakSet`, `WeakRef` and `FinalizationRegistry`. Namespace the keys you register.
- Symbol-keyed properties are not enumerated by `for...in`, are not returned by `Object.getOwnPropertyNames()`, and are ignored by `JSON.stringify()`. Find them with `Object.getOwnPropertySymbols()`.
- Symbols give only weak encapsulation; for real privacy use `#private` fields.
- `new Symbol()` throws `TypeError`. `String(sym)` works; `Symbol("foo") + "bar"` throws `TypeError`.

Self-check: `Symbol("foo") === Symbol("foo")` is false.

## Checked

Date: 2026-11-03. Confirmed on MDN Global_Objects/Symbol: uniqueness, Symbol.for/keyFor semantics and inverse example, registry symbols not garbage collectable and disallowed in weak collections, for...in, getOwnPropertyNames, getOwnPropertySymbols, JSON.stringify, new Symbol TypeError, String(sym) and concatenation behaviour, weak encapsulation wording. Removed as not stated there: keyFor returning undefined, Object.keys, Reflect.ownKeys symbol claim, "process-global" wording.

Method: documentation only; no commands were run.
