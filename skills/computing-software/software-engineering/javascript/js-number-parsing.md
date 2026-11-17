---
id: computing-software.software-engineering.javascript.js-number-parsing
name: js-number-parsing
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, number-parsing, js-numbers]
level: practitioner
status: docs-checked
description: "Parse integers with parseInt: radix rules, 0x handling, trailing-character behaviour, NaN checks, and why parseInt is not Math.trunc or BigInt."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/parseInt"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parsing integers with parseInt

- `parseInt(string, radix)` converts the first argument to a string, parses it, and returns an integer or `NaN`. Leading whitespace is ignored. `radix` is an integer from 2 to 36; a nonzero value outside that range gives `NaN`.
- Radix 0 or omitted does not always mean 10: a string starting with `0x`/`0X` (after whitespace and sign) is read as hex, otherwise radix 10. Prefixes like `0b` are treated as ordinary digits and a leading `0` is not octal. Pass the radix explicitly; use `Number()` or `BigInt()` for those prefixes.
- Parsing stops at the first character that is not a valid digit in the radix and returns what was parsed so far: `parseInt("15px", 10)` is 15, `parseInt("1e3", 10)` is 1, `parseInt("15,123", 10)` is 15, `parseInt("123_456")` is 123. If the first character is invalid the result is `NaN` (`parseInt("546", 2)`).
- `parseFloat()` parses `1e3` to 1000. `parseInt()` and `parseFloat()` differ only in parsing, not necessarily in return value (`parseInt("42")` and `parseFloat("42")` are both 42).
- Check results with `Number.isNaN`; `NaN` propagates through arithmetic.
- Do not use `parseInt` as a substitute for `Math.trunc()`: numbers at or above `1e+21` or at or below `1e-7` stringify in exponent form, so `parseInt(0.0000001, 10)` is 1 and `parseInt(1e21, 10)` is 1.
- Results outside the safe integer range lose precision; `BigInt("900719925474099267")` parses arbitrarily long integers. `parseInt` stops at a trailing `n`.
- `thatNumber.toString(radix)` converts a number to a string in a radix.

Self-check: run `["15px", "0xF", "1e3", "546"].map((s) => parseInt(s, 10))`.

## Checked

Confirmed against MDN "parseInt()" (page last modified 2025-07-08), read 2026-11-08. Removed: all `Number()` coercion results, the `Number.isFinite` vs `isFinite` advice, the Intl.NumberFormat separator tip and the `parseInt(0.0000005)` example (the page gives other values of the same behaviour), since those depend on pages not cited.
Method: docs-only read of cited pages, 2026-11-08
