---
id: computing-software.software-engineering.nim.overloading-forward-declarations
name: overloading-forward-declarations
category: computing-software
field: software-engineering
product: nim
tags: [overloading-forward-declarations, procedures-basics, overload, forward-declaration, mutual-recursion, operator, proc, nim]
level: practitioner
status: docs-checked
description: "Overload Nim procs by parameter types, define operators, and use forward declarations for mutual recursion."
sources:
  - https://nim-lang.org/docs/manual.html
  - https://nim-lang.org/docs/tut1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Overloading and forward declarations

Goal: overload and order procs correctly.

- Procs may share a name when their parameter types differ; the compiler chooses the most appropriate proc, and ambiguous calls are reported as errors (the manual: "ambiguous matches produce a compile-time error").
- Each operator such as `+` is just an overloaded proc. Define a new one by enclosing it in backticks: ``proc `$` (x: myDataType): string``. Call an operator like any proc with backticks too: `` `+`(3, 4) ``.
- Operators are used in infix or prefix form; an infix operator receives two arguments, a prefix operator one, and there are no postfix operators. The precedence of a user-defined operator is determined by its first character.
- Every variable and procedure must be declared before use. For mutual recursion give a forward declaration: write the signature and omit the `=` and the body, for example `proc even(n: int): bool`, then define `odd` and later `even`.
- A proc body can be a single expression whose value is returned implicitly.

Gotcha: user-defined operators are allowed but unusual ones such as `@!?+~` reduce readability.

Verify: calling `even(10)` and `odd(7)` across the forward declaration compiles and returns true.

## Checked

2026-11-08. Read the Nim tutorial Overloaded procedures, Operators and Forward declarations sections in full and the manual statement on ambiguous overload matches.

Removed as unconfirmed: the exact preference order of exact over generic over conversion matches in one line, the no-overload-on-return-type rule, the identical-pragmas requirement for forward declarations, and the stdlib shadowing note. Dropped the lib index source (not used).

Method: documentation only; no commands were run.
