---
id: computing-software.software-engineering.d.d-is-expression-and-compile-time-checks
name: d-is-expression-and-compile-time-checks
category: computing-software
field: software-engineering
product: d
tags: [d-is-expression-and-compile-time-checks, expressions, is-expression, traits-compiles, type-test, static-assert, d]
level: advanced
status: docs-checked
description: "Use is(T == U), is(T : U), is(T U == ...) patterns and is(typeof(expr)) / __traits(compiles) to test types and validity at compile time."
sources:
  - https://dlang.org/spec/expression.html
  - https://dlang.org/spec/traits.html
  - https://dlang.org/spec/version.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# is() expressions and __traits(compiles) tests

Goal: query types and code validity at compile time.

- `is(T == int)` compares types for equivalence; `is(T : int)` tests implicit conversion; `is(T == struct)`, `is(T == class)`, `is(T == enum)`, `is(T == function)`, `is(T == delegate)`.
- Pattern: `static if (is(T U == U[]))` captures the element type; `is(T == X!U, U)` deduces template args.
- `is(typeof(expr))` is true if expr is valid, e.g. `enum hasLength(R) = is(typeof(R.init.length));`
- `__traits(compiles, { ... })` checks whether a snippet compiles.
- `static assert(cond, "message")` fails the build.
- Templates constraints: `if (is(typeof(r.front)))`.

Gotchas:
- `Type` in an `is` expression must be syntactically correct but need not be semantically correct; if it is not, the condition is simply false.

Verify: `static assert(is(int[] == int[]) && !is(int : string));`

## Checked
Checked 2026-11-03 against the D spec Expressions page (IsExpression forms and type specialisations), the Traits page (`compiles`) and the Conditional Compilation page (`static assert`). Removed: the qualifier-stripping pattern, the claim that `__traits(compiles)` masks typos or does not swallow parse errors, and the class-conversion direction remark (not stated there).

Method: documentation only; no commands were run.
