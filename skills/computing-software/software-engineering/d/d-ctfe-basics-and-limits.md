---
id: computing-software.software-engineering.d.d-ctfe-basics-and-limits
name: d-ctfe-basics-and-limits
category: computing-software
field: software-engineering
product: d
tags: [d-ctfe-basics-and-limits, ctfe, compile-time, __ctfe, enum-init, constant-folding, compile-time-evaluation, d]
level: practitioner
status: docs-checked
description: "Run functions at compile time (CTFE) in the contexts the spec lists, know the documented CTFE restrictions, and branch with __ctfe."
sources:
  - https://dlang.org/spec/function.html
  - https://dlang.org/spec/attribute.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CTFE: what runs at compile time and its limits

Goal: use ordinary D functions at compile time.

- A function is evaluated at compile time where a compile-time value is required: initialisers of global/static variables and manifest constants (`enum t = buildTable(256);`), static array dimensions, template value arguments, `static if`, `static foreach`, `static assert`, `mixin`, `pragma` and `__traits` arguments. The function must have a body.
- Restrictions: no reference to mutable global or static variables, no inline asm, no non-portable casts (such as `int[]` to `float[]`), no reinterpreting overlapped union fields, no undefined behaviour, and no non-recoverable errors such as assert failures. Pointer arithmetic is only allowed on pointers into arrays. The restrictions apply only to code that is actually evaluated.
- `__ctfe` is true during CTFE and false otherwise, which gives an alternative path around forbidden operations; it cannot be read in a compile-time context such as a `static if` condition. `@__ctfe` marks a function that is only called with CTFE.

Gotchas:
- CTFE can take considerably longer than run time, and an infinite loop may hang the compiler.
- Results can differ from run time where behaviour is implementation defined.

Verify: `enum x = fib(20); static assert(x == 6765);`

## Checked
Checked 2026-11-03 against the D spec Functions page (Compile Time Function Execution, Run Time Values during CTFE) and the Attributes page (`@__ctfe`). Removed: the allowed-constructs list, the "forbidden: I/O, GC ops" list, the CTFE stack-trace remark and the enum/immutable tip (not stated there).

Method: documentation only; no commands were run.
