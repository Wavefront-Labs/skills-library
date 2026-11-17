---
id: computing-software.software-engineering.v-lang.v-const-declarations
name: v-const-declarations
category: computing-software
field: software-engineering
product: v-lang
tags: [v-const-declarations, const-and-globals, const, constants, pub const, const block, compile-time constant, v-lang]
level: intro
status: docs-checked
description: "Declare module-level constants with const, grouped blocks, typed and computed constants, and pub const exports."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Constants

Goal: define immutable module-level values.

- `const pi = 3.14` and `const world = '世界'`; a single constant can be declared separately: `const e = 2.71828`.
- Constants can only be defined at module level (outside functions) and can never be changed.
- V constants are more flexible than most: values can be arrays (`const numbers = [1, 2, 3]`), struct literals (`const red = Color{ r: 255, g: 0, b: 0 }`) and function calls (`const blue = rgb(0, 0, 255)`). Function calls are currently evaluated at program start-up (the docs mark compile-time evaluation as work in progress).
- Public: `pub const golden_ratio = 1.61803`. `pub` is only allowed before the `const` keyword and cannot be used inside a `const ( )` block.
- Inside the defining module a constant is used unqualified (or qualified with the module name); from another module prefix it with the module name, for example `math.pi`.
- Constant names must use `snake_case`.
- A constant initializer may call a function with the same name (`const answer = answer()`), but reading the constant itself in its initializer is a cycle.
- Constants are useful partly because global variables are not normally allowed.

Verify: attempt to assign to a constant and confirm the compiler rejects it.

## Checked

Date: 2026-11-02. Confirmed in the V documentation (doc/docs.md, "Constants", "Required module prefix"). Removed as not stated there: the `const ( ... )` grouped example, typed `u64(1) << 40`, `$d()` overrides, the const-array `<<` gotcha, "initialisation order" and "circular references are errors" details beyond the self-read cycle.

Method: documentation only; no commands were run.
