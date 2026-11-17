---
id: computing-software.software-engineering.javascript.js-symbol-hasinstance
name: js-symbol-hasinstance
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, symbol-hasinstance, js-symbols]
level: advanced
status: docs-checked
description: "Customise instanceof with Symbol.hasInstance; know what toStringTag, isConcatSpreadable and species hook."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol/hasInstance", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Customising operators with well-known symbols

- A static `[Symbol.hasInstance](instance)` method on the right-hand side of `instanceof` is called with the object, and its result is coerced to a boolean. Without one, `Function.prototype[Symbol.hasInstance]()` decides.
- `instanceof` throws `TypeError` if the right-hand side is not an object, or if its `Symbol.hasInstance` is not `null`, `undefined` or a function.
- `Symbol.toStringTag` supplies the default description used by `Object.prototype.toString()`.
- `Symbol.isConcatSpreadable` is a boolean saying whether an object is flattened to its array elements by `Array.prototype.concat()`.
- `Symbol.species` names the constructor function used to create derived objects.
- Keep these rare: they change semantics readers assume.

Example from MDN: `class MyArray { static [Symbol.hasInstance](instance) { return Array.isArray(instance); } }` makes `[] instanceof MyArray` true.

## Checked

Date: 2026-11-03. Confirmed on MDN Symbol/hasInstance (algorithm, TypeError conditions, example) and Global_Objects/Symbol (toStringTag, isConcatSpreadable, species descriptions). Removed as not stated there: the `[object MyThing]` output, array-likes, map/filter/slice and Promise species details, and the Even self-check.

Method: documentation only; no commands were run.
