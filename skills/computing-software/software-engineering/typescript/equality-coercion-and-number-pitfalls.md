---
id: computing-software.software-engineering.typescript.equality-coercion-and-number-pitfalls
name: equality-coercion-and-number-pitfalls
category: computing-software
field: software-engineering
product: typescript
tags: [javascript, type-coercion, floating-point-js, strict-equality, nan, bigint, number-precision, nullish-coalescing, object-is, money-handling]
level: practitioner
status: docs-checked
description: "Avoid JavaScript equality and number bugs: == coercion, NaN, -0, floating-point money math, MAX_SAFE_INTEGER and BigInt, || vs ??, and parseInt traps."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Equality_comparisons_and_sameness
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/MAX_SAFE_INTEGER
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/parseInt
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Nullish_coalescing
  - https://eslint.org/docs/latest/rules/eqeqeq
  - https://typescript-eslint.io/rules/prefer-nullish-coalescing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Equality, coercion and number pitfalls

**Goal:** comparisons and arithmetic that do what they look like they do.

## Equality
- Always `===` / `!==` (lint `eqeqeq`). `==` coerces: `"0" == false`, `[] == false`,
  `null == undefined` all true. The one accepted exception: `x == null` to test for
  null OR undefined (`eqeqeq: ["error", "smart"]`).
- `NaN !== NaN`. Test with `Number.isNaN(x)`, not global `isNaN("abc")` (coerces -> true).
- `Object.is(a, b)` distinguishes `-0` and `+0` and treats NaN as equal to itself.
- Objects/arrays compare by reference: `[1] === [1]` is false. Compare structurally
  with a deep-equal helper or by key.

## Defaults: || vs ??
```ts
const port = opts.port || 3000;   // 0 becomes 3000 (bug)
const port = opts.port ?? 3000;   // only null/undefined replaced
```
Same for `||=` vs `??=`. Use `?.` for optional chaining.

## Floating point
`0.1 + 0.2 === 0.30000000000000004`. For money: store integer minor units (cents) or use
a decimal library. Format with `Intl.NumberFormat`.
Compare floats with a tolerance: `Math.abs(a - b) < Number.EPSILON * scale`.

## Large integers
Numbers are float64: integers above `Number.MAX_SAFE_INTEGER` (2^53 - 1) lose
precision. 64-bit database ids MUST travel as strings in
JSON, or be parsed as `BigInt`. `JSON.parse` silently rounds them.
BigInt: `10n ** 20n`; cannot mix with Number in arithmetic; `JSON.stringify` throws on it.

## Parsing
- `parseInt("08")` is 8, but `parseInt("1e3")` is 1 and `parseInt(0.0000005)` is 5.
  Use `Number(str)` and check `Number.isFinite`, or always pass radix.
- `Number("")` is 0 and `Number(" ")` is 0: validate emptiness first.

## Truthiness traps
Falsy: `false, 0, -0, 0n, "", null, undefined, NaN`. `if (count)` skips zero;
`if (arr)` is always true even when empty (use `arr.length`).

## Verify
- [ ] eslint `eqeqeq` and `@typescript-eslint/prefer-nullish-coalescing` enabled.
- [ ] Money and id fields have tests with values like 0.1+0.2 and 9007199254740993.

## Checked
Checked 2026-10-25 against the MDN content repository, the ESLint eqeqeq rule page and the typescript-eslint rule docs. Confirmed: strict equality versus NaN/-0/+0 handling, global isNaN coercing versus Number.isNaN, `Object.is`; the eqeqeq `smart` option allowing comparison against null; `??` versus `||`; Number.EPSILON and MAX_SAFE_INTEGER; parseInt returning a one-digit result for very small numbers (for example 1e-7 gives 1); BigInt cannot be mixed with Number and JSON.stringify rejects BigInt; the falsy list including 0n; Number() ignoring whitespace. Removed the unconfirmed Date parsing claim and the named decimal libraries.
Method: documentation only; no commands were run.
