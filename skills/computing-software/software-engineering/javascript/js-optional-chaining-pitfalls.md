---
id: computing-software.software-engineering.javascript.js-optional-chaining-pitfalls
name: js-optional-chaining-pitfalls
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, optional-call, js-optional-chaining]
level: practitioner
status: docs-checked
description: "Optional chaining pitfalls: short-circuit scope, grouped chains, non-function properties, invalid targets, undeclared roots, and the nullish-only check."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Optional_chaining"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Optional chaining pitfalls

- `?.` short-circuits only for `null` or `undefined`: the expression evaluates to `undefined` and the rest of that continuous chain is not evaluated. `potentiallyNullObj?.a.b` does not throw, and `obj?.[x++]` does not evaluate `x++` when `obj` is nullish.
- Grouping breaks the chain: `(potentiallyNullObj?.a).b` throws `TypeError: Cannot read properties of undefined (reading 'b')`.
- `?.` guards only the position where it is written. If `someInterface` itself may be nullish use `someInterface?.customMethod?.()`.
- If a property exists but is not a function, `obj.method?.()` still raises a `TypeError` ("is not a function"). `?.` checks nullishness, not type.
- Unlike `obj.first && obj.first.second`, `?.` does not short-circuit on other falsy values such as `0`; the `&&` form would return `0`.
- Invalid forms: assignment `object?.property = 1` (SyntaxError, invalid left-hand side), tagged templates `String.raw?.\`...\``, and `new` constructors `new Intl?.DateTimeFormat()` or `new Map?.()`.
- A non-declared root is still a `ReferenceError` (`undeclaredVar?.prop`), though a root with value `undefined` is fine.
- Bracket form `arr?.[42]` and call form `func?.(args)` exist; combine with `??` for defaults, as in `customer?.city ?? "Unknown city"`.
- Overuse can hide contract violations: use it for data that is genuinely optional.

Self-check: `({}).a?.b` is `undefined` while `({}).a.b` throws a `TypeError`.

## Checked

Confirmed against MDN "Optional chaining (?.)" , read 2026-11-08. Removed: the claim that `a?.b === null` can be false (not on the page, though it follows from `undefined`), and the transpiled-output performance remark. The overuse remark is advice, not a factual claim.
Method: docs-only read of cited pages, 2026-11-08
