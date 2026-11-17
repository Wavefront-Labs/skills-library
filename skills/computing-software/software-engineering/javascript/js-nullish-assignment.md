---
id: computing-software.software-engineering.javascript.js-nullish-assignment
name: js-nullish-assignment
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, logical-assignment, js-optional-chaining]
level: practitioner
status: docs-checked
description: "Use ?? to default only null and undefined instead of ||; know the mixing rule and how ?? pairs with ?. ."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Nullish_coalescing"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nullish coalescing

- `a ?? b` returns `b` only when `a` is `null` or `undefined`; `a || b` also replaces any falsy value (`0`, `""`, `NaN`, `false`), so `count || 42` gives 42 for a count of 0 while `count ?? 42` gives 0.
- Combining `??` directly with `||` or `&&` throws a `SyntaxError`; add parentheses, e.g. `(null || undefined) ?? "foo"`.
- `??` has the fifth-lowest operator precedence, directly lower than `||` and directly higher than the conditional (ternary) operator.
- It short-circuits: the right side is evaluated only when needed.
- With optional chaining: `foo.someBarProp?.toUpperCase() ?? "not available"` gives a default when the property is missing.
- The related `??=` operator is covered on MDN's logical assignment page.

Self-check: `0 ?? 42` is 0 but `0 || 42` is 42.

## Checked

Date: 2026-11-03. Confirmed on MDN Operators/Nullish_coalescing: null/undefined-only fallback, difference from `||`, SyntaxError and parentheses, precedence, short-circuiting section, optional chaining pairing. Removed as not stated there: the semantics of `||=` and `&&=` (the page only links `??=`), setter skipping, optional call and index forms, and `delete a?.b`; the title and description now cover `??` only.

Method: documentation only; no commands were run.
