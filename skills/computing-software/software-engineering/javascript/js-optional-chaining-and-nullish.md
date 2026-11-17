---
id: computing-software.software-engineering.javascript.js-optional-chaining-and-nullish
name: js-optional-chaining-and-nullish
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-optional-chaining, nullish-coalescing, logical-assignment, falsy-values]
level: intro
status: docs-checked
description: "Use ?., ??, ??= correctly and avoid || defaults that swallow 0 and empty strings."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Optional_chaining", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Nullish_coalescing"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Optional chaining and nullish coalescing

- `a?.b` and `f?.()` short-circuit the whole chain to `undefined` when the left side is `null` or `undefined`.
- `x ?? d` falls back only on `null`/`undefined`; `x || d` falls back on any falsy value, which wrongly replaces `0`, `""` and `false`.
- `??=` is nullish coalescing assignment (see the Nullish_coalescing page for the other logical assignment operators).
- Combining `??` directly with `&&` or `||` without parentheses is a SyntaxError.
- An optional chain cannot be an assignment target (`object?.property = 1` is a SyntaxError) and cannot be the constructor of a `new` expression.
- Do not chain on values that should never be missing: optional chaining hides bugs. Check the type contract first.

## Checked

Date: 2026-11-02. Confirmed on MDN (Operators/Optional_chaining, Operators/Nullish_coalescing): short-circuit to undefined, optional call, ?? vs ||, ??= existence, ?? mixing SyntaxError, assignment and new restrictions. Removed as not stated there: `a?.[k]` detail, `delete a?.b`, and the setter-skipping behaviour of logical assignment (not read).

Method: documentation only; no commands were run.
