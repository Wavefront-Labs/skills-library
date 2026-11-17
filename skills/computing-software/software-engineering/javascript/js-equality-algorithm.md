---
id: computing-software.software-engineering.javascript.js-equality-algorithm
name: js-equality-algorithm
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, loose-equality-algorithm, js-type-coercion]
level: practitioner
status: docs-checked
description: "How == coerces operands per the ECMAScript IsLooselyEqual steps, the null/undefined case, and how Object.is differs for NaN and -0."
sources:
  - https://tc39.es/ecma262/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loose equality algorithm (==)

- `==` runs IsLooselyEqual (ECMA-262 7.2.13). If both operands have the same type it returns the result of IsStrictlyEqual (the `===` rule).
- `null == undefined` and `undefined == null` are true. No other step makes `null` or `undefined` loosely equal to anything, so `null == 0` is false.
- Number vs String: the String is converted with ToNumber, so `"1" == 1` is true.
- Boolean vs anything: the Boolean is converted with ToNumber first (`true` becomes 1, `false` becomes 0) and the comparison repeats.
- A String, Number, BigInt or Symbol against an Object: the Object goes through ToPrimitive and the comparison repeats.
- BigInt vs String converts the String with StringToBigInt (no valid conversion means false). BigInt vs a finite Number is true only when the mathematical values are equal.
- Worked from those steps: `[] == false` is true (false becomes 0, `[]` becomes `""` through ToPrimitive, `""` becomes 0). `NaN == NaN` is false because Number::equal returns false when either side is NaN.
- `Object.is` returns SameValue: `Object.is(NaN, NaN)` is true and `Object.is(0, -0)` is false (Number::sameValue), while `NaN === NaN` is false and `0 === -0` is true (Number::equal).
- Avoid comparing to booleans (`x == true`); because of the Boolean-to-number step, test truthiness or an explicit value instead.

Self-check: predict `"1" == 1` (true), `null == 0` (false), `[] == false` (true), then confirm in a console.

## Checked

Checked 2026-11-08 against the ECMAScript specification (tc39.es/ecma262): 7.2.13 IsLooselyEqual, 7.2.14 IsStrictlyEqual, Number::equal and Number::sameValue, Object.is (20.1.2.15). Removed: the ESLint `eqeqeq` option claim and the `null >= 0` claim (not in the cited page).
Method: docs-only read of cited pages, 2026-11-08
