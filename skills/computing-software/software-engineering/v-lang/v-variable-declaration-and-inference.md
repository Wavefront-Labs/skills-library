---
id: computing-software.software-engineering.v-lang.v-variable-declaration-and-inference
name: v-variable-declaration-and-inference
category: computing-software
field: software-engineering
product: v-lang
tags: [v-variable-declaration-and-inference, variables-and-mutability, variables, type inference, declaration, assignment, zero value, v-lang]
level: intro
status: docs-checked
description: "Declare variables with :=, rely on type inference, assign with =, mark mut, swap values and understand the unused-variable and shadowing rules."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Declaring variables with := and type inference

Goal: declare and initialise variables correctly.

- `name := 'Bob'` declares and infers the type; `age := 20` is `int`; `1.0` literals are `f64`. Variables are declared and initialized with `:=`, the only way to declare one, so they always have an initial value.
- Change a variable with `=` only if it was declared `mut`; variables are immutable by default.
- `=` assigns to an existing variable; assigning to an undeclared name does not compile.
- Choose another type by conversion: `i64(9999999999)`, `f32(3.14)`.
- Swap without a temporary: `a, b = b, a`.
- Variables may only be defined inside functions; globals are off by default.
- Names use `snake_case`; type names use `PascalCase`.
- An unused variable gives a warning in development mode and a compile error with `-prod`; use `_` for an unneeded loop index, key or value or an ignored return value.
- Shadowing is not allowed: redeclaring a name used in a parent scope is a compile error.

Verify: compile a file with `mut a := 0; a = 1` and one without `mut` to see the error.

## Checked

Date: 2026-11-03. Confirmed in the V documentation (doc/docs.md, "Variables", "Mutable variables", "Initialization vs assignment", "Warnings and declaration errors", "Primitive types"). Removed: `a, b := 1, 'x'` multi-declaration, the `mut n := int(0)` and `[]u8{}` zero-value examples, the claim that unused variables are always errors (the docs say warning in development mode, error with `-prod`), and the `_ = x` workaround.

Method: documentation only; no commands were run.
