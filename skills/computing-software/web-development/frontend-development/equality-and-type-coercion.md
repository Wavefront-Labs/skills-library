---
id: computing-software.web-development.frontend-development.equality-and-type-coercion
name: equality-and-type-coercion
category: computing-software
field: web-development
product: frontend-development
tags: [type-coercion, object-is, loose-equality, samevaluezero, number-conversion, javascript]
level: practitioner
status: verified
description: "JavaScript equality algorithms (==, ===, Object.is, SameValueZero), coercion rules that cause bugs, and safe number and boolean conversion."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Equality_comparisons_and_sameness
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number#number_coercion
  - https://tc39.es/ecma262/#sec-islooselyequal
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Equality and type coercion

## 1. Four sameness algorithms
| Algorithm | Used by | NaN equals NaN | +0 equals -0 |
|---|---|---|---|
| `===` strict | most code, `indexOf`, `switch` | no | yes |
| `==` loose | legacy | no | yes |
| SameValueZero | `includes`, `Map`/`Set` keys | yes | yes |
| `Object.is` (SameValue) | React state bail-out, `useEffect` deps | yes | no |
```js
[NaN].indexOf(NaN);   // -1
[NaN].includes(NaN);  // true
Object.is(0, -0);     // false
```

## 2. The only `==` worth keeping
`x == null` is true for exactly `null` and `undefined`. Everything else: use `===` (enforce with ESLint `eqeqeq: ["error", "smart"]`).
Traps: `"" == 0`, `"0" == false`, `[] == false` are all `true`; `null == 0` is `false`.

## 3. Conversion rules that bite
```js
Number("")        // 0   (empty input becomes zero!)
Number(" 12 ")    // 12
Number("12px")    // NaN, parseInt("12px", 10) -> 12
Number(null)      // 0,  Number(undefined) -> NaN
"5" + 2           // "52"  (+ prefers strings)
"5" * 2           // 10
!!"false"         // true  (non-empty string)
typeof null       // "object"
```
Safe form parsing:
```js
const raw = input.value.trim();
const n = raw === "" ? null : Number(raw);
if (n !== null && !Number.isFinite(n)) throw new Error("not a number");
```
Use `Number.isNaN` (no coercion) not global `isNaN("abc")` (true). Use `Number.isInteger`, `Number.isSafeInteger` for ids; above 2^53 use `BigInt` or strings.

## 4. `||` vs `??`
`count || 10` replaces `0` and `""`; `count ?? 10` replaces only `null`/`undefined`. Same for `||=` vs `??=`.

## 5. Objects
Objects compare by reference: `{a:1} === {a:1}` is false. Deep-compare with a library or `node:util.isDeepStrictEqual` in Node; never `JSON.stringify` comparison (key order, undefined, Dates).

Run in Node 20: `[NaN].indexOf(NaN)` -1, `includes` true, `Object.is(0, -0)` false, `new Set([NaN, NaN]).size` 1; `"" == 0`, `"0" == false`, `[] == false` true, `null == 0` false; `Number("")` 0, `Number(" 12 ")` 12, `Number("12px")` NaN, `parseInt("12px", 10)` 12, `Number(null)` 0, `Number(undefined)` NaN, `"5" + 2` `"52"`, `"5" * 2` 10, `!!"false"` true, `isNaN("abc")` true but `Number.isNaN("abc")` false, `Number.isSafeInteger(2**53)` false, `0 || 10` 10 vs `0 ?? 10` 0, `util.isDeepStrictEqual` true for equal objects while `JSON.stringify` comparison was false for reordered keys.

## Verify
- [ ] ESLint `eqeqeq` and `no-implicit-coercion` enabled.
- [ ] Numeric inputs handle "", "0", "1e3", "abc" correctly in tests.
