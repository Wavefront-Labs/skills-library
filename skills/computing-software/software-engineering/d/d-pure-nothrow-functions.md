---
id: computing-software.software-engineering.d.d-pure-nothrow-functions
name: d-pure-nothrow-functions
category: computing-software
field: software-engineering
product: d
tags: [d-pure-nothrow-functions, function-attributes, pure, nothrow, weakly-pure, strongly-pure, attribute-inference, side-effects, d]
level: practitioner
status: docs-checked
description: "Mark functions pure and nothrow, and understand weakly versus strongly pure functions and the debug-statement exception."
sources:
  - https://dlang.org/spec/function.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pure and nothrow functions

Goal: declare and rely on purity and nothrow.

- `pure`: cannot access global or static mutable state (reading immutable globals is fine) and can only call pure functions; it can modify local state and throw exceptions. A weakly pure function has parameters with mutable indirections; a strongly pure one has none and cannot modify external state, and an implementation may memoize calls to it.
- `nothrow`: such functions can only throw exceptions derived from `Error`.
- Some function attributes can be inferred.
- Impure code is allowed inside a `debug` statement of a pure function (`debug writeln("i = ", i);`).
- Group syntax: `pure nothrow @safe:` as a label, or per-function.

Gotchas:
- A pure function can only call pure functions, so calling `writeln` needs a `debug` statement or returning a string instead.

Verify: remove an attribute from a callee and see the error naming the offending call.

## Checked
Checked 2026-11-03 against the D spec Functions page (Function Attributes, Pure Functions, Strong vs Weak Purity, Debugging, Nothrow Functions). Removed: the `Exception`/`Throwable` try-catch rule, the `to!int` remark and the attribute-inference details beyond "some can be inferred".

Method: documentation only; no commands were run.
