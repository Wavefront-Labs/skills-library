---
id: computing-software.software-engineering.javascript.js-truthiness-toprimitive
name: js-truthiness-toprimitive
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, toprimitive, js-type-coercion]
level: practitioner
status: docs-checked
description: "Control object-to-primitive conversion with Symbol.toPrimitive and know the falsy list."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol/toPrimitive", "https://developer.mozilla.org/en-US/docs/Glossary/Falsy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ToPrimitive and truthiness rules

- Falsy values (MDN's complete list): `null`, `undefined`, `false`, `NaN`, `0`, `-0`, `0n`, `""` and `document.all`, the only falsy object. Everything else is truthy.
- All type coercion algorithms look up `Symbol.toPrimitive` on an object first; it is called with a string `hint` of `"number"`, `"string"` or `"default"`. Without it, `valueOf()` and `toString()` are called in different orders.
- The `"number"` hint is used by numeric coercion (unary `+`), `"string"` by string coercion (template literals), and `"default"` by the primitive coercion algorithm (for example `obj + ""`).
- The hint is only a weak signal of preference. The method must return a primitive, or a `TypeError` is thrown.
- `Date.prototype[Symbol.toPrimitive]()` treats `"default"` as `"string"`, so a Date in `+` concatenates as text.
- `Symbol.prototype[Symbol.toPrimitive]()` ignores the hint and always returns the symbol; convert symbol objects to strings explicitly with `String()`.
- Define `[Symbol.toPrimitive](hint)` on value classes for full control instead of juggling `valueOf` and `toString`.

Self-check: `+{ [Symbol.toPrimitive]: h => h === "number" ? 5 : 0 }` gives 5, and `` `${obj}` `` on an object that returns a fixed string for hint `"string"` yields that string.

## Checked

2026-11-08. Confirmed on MDN Symbol.toPrimitive (lookup order, three hints and which algorithm uses each, TypeError on non-primitive result, Date and Symbol exceptions, the example with `+obj`) and on MDN Falsy (the full falsy list). Removed the claim that a "throwing" conversion message reads `Cannot convert object to primitive value`, and the claim that `"0"`, `[]` and `{}` are truthy beyond the list "everything else", since neither page spells them out.

Method: docs-only read of cited pages, 2026-11-08
