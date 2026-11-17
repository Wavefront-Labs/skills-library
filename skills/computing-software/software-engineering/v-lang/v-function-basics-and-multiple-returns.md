---
id: computing-software.software-engineering.v-lang.v-function-basics-and-multiple-returns
name: v-function-basics-and-multiple-returns
category: computing-software
field: software-engineering
product: v-lang
tags: [v-function-basics-and-multiple-returns, functions, fn, multiple return values, tuple, destructuring, return, v-lang]
level: intro
status: docs-checked
description: "Declare functions with fn, typed params and return types, return several values, ignore one with _, and pass mut arguments for arrays and maps."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Function declarations and multiple return values

Goal: write and call functions idiomatically.

- `fn add(x int, y int) int { return x + y }`; the type comes after the argument name. When a signature spans several lines, commas between parameters are optional.
- Multiple returns: `fn foo() (int, int) { return 2, 3 }` then `a, b := foo()`. Use `_` to ignore one: `c, _ := foo()`.
- Functions can be used before their declaration (hoisting), which is true of all declarations in V.
- Functions cannot be overloaded, as in Go and C.
- Arguments are immutable by default. Mark a parameter `mut` and repeat `mut` at the call site: `fn multiply_by_2(mut arr []int)` is called as `multiply_by_2(mut nums)`.
- V does not allow modifying primitive-type arguments such as integers through `mut`; only more complex types such as arrays and maps. Prefer returning values (`user = register(user)`) over mutating arguments.
- Variadic: `fn sum(a ...int) int`, spread an array with `sum(...a)`.
- Functions are private by default; `pub` makes them usable from other modules (only inside a named module).
- Immutable struct arguments may be passed by value or by reference at the compiler's choice; write `&Foo` to force a reference.

Gotchas:
- The call site must repeat `mut` for mutable arguments.

Verify: compile and print the results of a tuple-returning call.

## Checked

Date: 2026-11-03. Confirmed in the V documentation (doc/docs.md, "Functions", "Hoisting", "Returning multiple values", "Symbol visibility", "Immutable function args by default", "Mutable arguments", "Variable number of arguments", "References"). Removed or corrected: the `fn add(x, y int)` shared-type form (not documented), and the example `fn inc(mut n int) { n++ }`, which contradicts the docs statement that V does not allow modifying primitive arguments.

Method: documentation only; no commands were run.
