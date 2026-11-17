---
id: computing-software.software-engineering.javascript.js-float-precision
name: js-float-precision
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, float-precision, js-numbers]
level: practitioner
status: docs-checked
description: "Handle 0.1+0.2, Number.EPSILON, MAX_SAFE_INTEGER, toFixed and Math.round rounding in JavaScript numbers."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/EPSILON", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/toFixed", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/round"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Floating point precision and safe integers

- A `Number` is an IEEE 754 double-precision 64-bit value (1 sign bit, 11 exponent bits, 52 mantissa bits), good for about 15 to 17 significant decimal digits. Binary cannot represent 0.1 exactly, so `0.1 + 0.2 === 0.3` is `false` (the sum is `0.30000000000000004`).
- Compare with a tolerance sized for the magnitude and accuracy of your data. `Number.EPSILON` (2^-52) is a reasonable threshold only for arithmetic around magnitude 1; MDN says not to use it blindly (for values near 2000 it scales the tolerance, e.g. `2000 * Number.EPSILON`).
- Integers are exact only from `Number.MIN_SAFE_INTEGER` to `Number.MAX_SAFE_INTEGER` (-(2^53 - 1) to 2^53 - 1); check with `Number.isSafeInteger`. Integers beyond that range in JSON can be corrupted by the parser; send them as strings or use `BigInt`.
- Money: prefer integer minor units (cents) or a decimal library over accumulating floats.
- `toFixed(digits)` returns a string and rounds the binary value; `digits` must be 0 to 100 or a `RangeError` is thrown. MDN shows `(2.55).toFixed(1)` giving `'2.5'` because the closest double is slightly lower.
- `Math.round` rounds exactly-half values toward +Infinity, so `Math.round(-5.5)` is `-5` and `Math.round(20.5)` is `21`. It returns `-0` for `-0.5 <= x < 0`.

Self-check: evaluate `0.1 + 0.2`, `Number.isSafeInteger(2**53)` and `Math.round(-5.5)` before relying on them.

## Checked

Confirmed on the cited MDN pages (Number, Number.EPSILON, toFixed, Math.round): encoding sizes, 0.1 + 0.2 result, EPSILON guidance, safe-integer range, JSON corruption note, toFixed range and the 2.55 example, Math.round half rule and -0 case. Removed: the fixed `1e-9` tolerance, the `1.005.toFixed(2)` example and the `9007199254740993` self-check, none of which the pages state.

Method: docs-only read of cited pages, 2026-11-08
