---
id: computing-software.software-engineering.javascript.js-numbers-bigint-and-math
name: js-numbers-bigint-and-math
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-numbers, bigint, number-epsilon, math-object]
level: practitioner
status: docs-checked
description: "Handle IEEE 754 doubles, BigInt, safe integers and rounding correctly in JavaScript."
sources: ["https://tc39.es/ecma262/", "https://developer.mozilla.org/en-US/docs/Web/JavaScript"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Numbers, BigInt and Math

- Every `Number` is a 64-bit double: `0.1 + 0.2 !== 0.3`. Compare with a tolerance (`Math.abs(a - b) < Number.EPSILON * scale`, where `Number.EPSILON` is the 2^-52 mantissa precision), or do money in integer minor units.
- Exact integers only up to `Number.MAX_SAFE_INTEGER` (2^53 - 1); check with `Number.isSafeInteger(n)`. Larger IDs from JSON lose precision, so keep them as strings.
- `BigInt` (`123n`, `BigInt("123")`) is arbitrary precision. It cannot mix with Number in arithmetic (`1n + 1` throws TypeError), `Math.*` rejects it, and `JSON.stringify` throws on it unless you add a `toJSON`/replacer.
- Division of BigInt truncates toward zero; `**` works; unary plus is not supported.
- Parsing: prefer `Number(str)` (strict: `Number("12px")` is NaN) over `parseInt` (stops at junk, needs a radix argument: `parseInt(s, 10)`).
- `NaN !== NaN`; use `Number.isNaN` (the global `isNaN` coerces first). `-0` exists; `Object.is(-0, 0)` is false.
- Rounding: `Math.round` rounds .5 toward +Infinity (`Math.round(-2.5)` is -2); `toFixed` returns a string and can round unexpectedly because many decimals are not exactly representable (MDN: `(2.55).toFixed(1)` is "2.5").
- Format for display with `Intl.NumberFormat`, never string-concatenate thousands separators.

Verify: run `0.1 + 0.2`, `9007199254740993`, and `1n + 1` in a console and confirm you handle each case.

## Checked

2026-11-02. Checked against MDN Number, BigInt, Math.round and Number.toFixed (64-bit double, EPSILON, BigInt cannot mix with Number or Math, division truncates toward zero, unary plus unsupported, Math.round half toward +Infinity so -2.5 gives -2, toFixed examples). Replaced the 1.005.toFixed(2) example with MDN's own example. Other claims (MAX_SAFE_INTEGER, isSafeInteger, NaN, Object.is(-0, 0), Number vs parseInt, Intl.NumberFormat) are standard ECMAScript behaviour described on the MDN pages above and tc39.es/ecma262.

Method: documentation only; no commands were run.
