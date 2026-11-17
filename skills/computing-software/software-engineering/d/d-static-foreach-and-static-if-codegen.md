---
id: computing-software.software-engineering.d.d-static-foreach-and-static-if-codegen
name: d-static-foreach-and-static-if-codegen
category: computing-software
field: software-engineering
product: d
tags: [d-static-foreach-and-static-if-codegen, mixins, static-foreach, static-if, static-assert, compile-time-loop, unrolling, declaration-generation, d]
level: advanced
status: docs-checked
description: "Generate declarations and unroll loops at compile time with static foreach, static if and static assert, including scoping and break rules."
sources:
  - https://dlang.org/spec/version.html
  - https://dlang.org/spec/traits.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# static foreach, static if and declaration generation

Goal: loop at compile time, even at module scope.

- `static foreach (i; iota(0, 3))` with a `mixin` body can declare `enum x0`, `x1`, `x2`, as in the spec.
- Iterates ranges, arrays and sequences; the bounds are evaluated at compile time and the body is copied once per element. The loop variable is a compile-time enum or alias, never a runtime variable.
- The body does not introduce a new scope, so it can add declarations to an existing scope; cases can be generated inside a `switch` (`static foreach (i; 0 .. 5) { case i: ... }`).
- `static if` works at module, class, template, struct, union and function scope and does not introduce a new scope even with `{ }`; chain with `else static if`.
- `static assert(0, "msg")` marks unreachable configurations.
- Combined with `__traits(allMembers, T)` and `__traits(getMember, T, name)` it replaces hand-written boilerplate.

Gotchas:
- Inside a function, use a second set of braces (`{{ ... }}`) to get a new scope for each expansion.
- `break` and `continue` cannot change the control flow of a `static foreach` itself; one inside an expanded `switch` needs an explicit label.

Verify: `static assert(x2 == 2);` after generating `x0..x2`.

## Checked
Checked 2026-11-03 against the D spec Conditional Compilation page (Static If, Static Foreach, Static Assert) and the Traits page (`allMembers`, `getMember`). Removed: the `stringof` digit remark and the `EnumMembers` switch example (not on those pages).

Method: documentation only; no commands were run.
