---
id: computing-software.software-engineering.nim.proc-parameters-result
name: proc-parameters-result
category: computing-software
field: software-engineering
product: nim
tags: [proc-parameters-result, procedures-basics, proc, result, return, parameters, default-arguments, named-arguments, nim]
level: intro
status: docs-checked
description: "Declare Nim procs with typed and default parameters, return via result or return, use named arguments and discard."
sources:
  - https://nim-lang.org/docs/manual.html
  - https://nim-lang.org/docs/tut1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proc parameters, result variable and defaults

Goal: write idiomatic procs.

```nim
proc area(w, h: float, scale = 1.0): float =
  result = w * h * scale
```
- A proc that returns a value has an implicit `result` variable, initialized to the type's default (binary zero); referential types are `nil` at the start and may need manual initialization. `return` with no expression is shorthand for `return result`, and the result is returned automatically at the end if there is no `return`.
- Do not redeclare `var result`: it would shadow the implicit variable.
- A proc without `return` or `result` returns the value of its last expression.
- Named arguments make order irrelevant: `createWindow(show = true, title = "x", ...)`; mixing them with positional ones is possible but not very readable. The compiler checks each parameter receives exactly one argument.
- Default values let callers pass only what differs, and type inference works for parameters with defaults (`title = "unknown"`).
- Command invocation: routines can be called without `()` if the call is syntactically a statement, and for expressions only a single argument may follow (`echo f 1, f 2` parses as `echo(f(1), f(2))`). Calls with no arguments still need `()`.
- Parameters are immutable inside the proc; declare a local `var` (shadowing is an idiom) or use a `var` parameter so the caller sees the change.
- Nim does not allow silently ignoring a return value: use `discard yes("...")`, or mark the proc `{.discardable.}`.

Verify: a proc returning without assigning result yields the zero value.

## Checked

2026-11-08. Read the Nim tutorial Procedures section in full (Result variable, Parameters, Discard statement, Named arguments, Default values) and the manual passages on return, the discardable pragma and command invocation syntax.

Removed as unconfirmed: the claim that default values are evaluated on each call, and the method-call example `w.area(h)` (not read in these sections). Dropped the lib index source (not used).

Method: documentation only; no commands were run.
