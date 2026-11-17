---
id: computing-software.software-engineering.v-lang.v-variadic-functions
name: v-variadic-functions
category: computing-software
field: software-engineering
product: v-lang
tags: [v-variadic-functions, functions, variadic, args, varargs, spread, fn, v-lang]
level: practitioner
status: docs-checked
description: "Accept a variable number of arguments with ...T parameters, pass slices with the spread form, and know the array semantics."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Variadic functions

Goal: write functions taking any number of same-typed arguments.

- A `...` prefix on a parameter type collects an arbitrary number of arguments into an array: `fn sum(a ...int) int { mut total := 0; for x in a { total += x }; return total }`.
- Call `sum()` (0), `sum(1)`, `sum(2, 3)`; pass an existing array with the prefix `...`: `a := [2, 3, 4]` then `sum(...a)` returns 9 ("array decomposition").
- Methods on generic structs can also accept variadic arguments; the receiver type determines the specialization.

Verify: `assert sum(1, 2, 3) == 6` and `assert sum() == 0`.

## Checked

Date: 2026-11-02. Confirmed in the V documentation (doc/docs.md, "Variable number of arguments"). Removed as not stated there: "variadic parameter must be last", `...Any` and interface advice for mixed types, the printf and "array without `...` is a type error" gotchas.

Method: documentation only; no commands were run.
