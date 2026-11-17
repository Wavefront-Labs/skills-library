---
id: computing-software.software-engineering.nim.variables-let-var-const
name: variables-let-var-const
category: computing-software
field: software-engineering
product: nim
tags: [variables-let-var-const, tutorial-basics, var, let, const, mutability, immutable, default-values, nim]
level: intro
status: docs-checked
description: "Choose between Nim var, let and const, grouped declarations, and compile-time evaluation of const."
sources:
  - https://nim-lang.org/docs/tut1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Variables: var, let and const

Goal: declare values with the right mutability.

- `var x, y: int` declares mutable variables; `let` works like `var` but declares single-assignment symbols that cannot change after initialization (`let x = "abc"` then `x = "xyz"` is illegal).
- `const x = "abc"` binds a symbol to a value that cannot change, and the compiler must be able to evaluate the expression at compile time; `const input = readLine(stdin)` is an error ("constant expression expected") while `let input = readLine(stdin)` works. The tutorial describes `const` as "enforce compile time evaluation and put it into a data section".
- Declarations can be grouped by indenting after `var` or `const`, with comments allowed between lines, for example `var` followed by indented `x, y: int` and `a, b, c: string` lines. Constants may compute from earlier constants: `z = y + 5`.
- Local type inference applies: `var name = readLine(stdin)` infers `string`; this is basically the only form of type inference in Nim.
- `var x, y = 3` assigns 3 to both variables, and later `x = 42` changes only `x`.
- Without a type suffix, integer literals are `int` and a literal with a dot is `float`; suffixes such as `0'i8` and `0.0'f32` pick other types. A `string` variable starts as the empty string `""`.

Verify: assigning to a `let` fails to compile.

## Checked

2026-11-08. Read the Nim tutorial sections The var statement, Constants, The let statement, The assignment statement, the first-program notes on type inference, and the Strings, Integers and Floats sections.

Removed as unconfirmed on the tutorial: the claim that `let` of a reference type still lets you mutate its fields, the zero-value list for uninitialized variables, the const VM and FFI limits, and the shadowing rules. Dropped the manual and lib index sources (not used).

Method: documentation only; no commands were run.
