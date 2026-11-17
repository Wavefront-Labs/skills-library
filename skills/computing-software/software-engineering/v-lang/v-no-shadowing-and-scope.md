---
id: computing-software.software-engineering.v-lang.v-no-shadowing-and-scope
name: v-no-shadowing-and-scope
category: computing-software
field: software-engineering
product: v-lang
tags: [v-no-shadowing-and-scope, variables-and-mutability, shadowing, scope, block scope, redeclaration, naming, v-lang]
level: practitioner
status: docs-checked
description: "Understand that V forbids variable shadowing, how block scope works, and how to rename or reuse names."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# No shadowing and block scope

Goal: avoid shadowing errors and structure scopes cleanly.

- Unlike most languages, variable shadowing is not allowed: declaring a variable with a name already used in a parent scope is a compile error (`error: redefinition of `a``), including for `a := 10` followed by `{ a := 20 }`.
- Field shadowing is allowed: a struct can declare `width` while an embedded `Dimension` also has `width`; `test.width` is the outer one and `test.Dimension.width` the embedded one.
- A local variable may not reuse the name of a global (`error: variable `devices` shadows a global variable`); the check covers declarations, function and lambda parameters, `for` variables, `if` guards, `select` receives and compile-time `$for` variables. `_` is left alone.
- Variable and function names must use `snake_case`; type names use `PascalCase`.
- Variables are only defined in functions; reassign with `mut` or choose a new name instead of redeclaring.
- `if v := m['foo'] { ... }` binds `v` only for the first branch; `err` is only in scope for the `else` branch of a result guard.
- Use `_` to ignore an unused loop index, key, value or returned value; unused variables give a warning in development and an error with `-prod`.

Verify: introduce a duplicate name and read the redefinition error.

## Checked

Date: 2026-11-02. Confirmed in the V documentation (doc/docs.md, "Warnings and declaration errors", "Variables", "Shadowing a global", "If unwrapping", "Handling options/results"). Removed as not stated there: shadowing of function params and imports specifically, the rejection of locals named like imported modules, loop-variable lifetime details, the `for i, item in items` rename advice.

Method: documentation only; no commands were run.
