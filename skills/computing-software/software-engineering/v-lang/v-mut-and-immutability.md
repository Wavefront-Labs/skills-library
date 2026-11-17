---
id: computing-software.software-engineering.v-lang.v-mut-and-immutability
name: v-mut-and-immutability
category: computing-software
field: software-engineering
product: v-lang
tags: [v-mut-and-immutability, variables-and-mutability, mut, immutable, mutable, immutability, reassign, v-lang]
level: intro
status: docs-checked
description: "Mark variables, parameters and receivers mutable with mut, and understand why immutability is the default."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mut and immutability by default

Goal: apply V's immutable-by-default rule.

- Variables are immutable by default; declare with `mut` to change them: `mut age := 20` then `age = 21`. `:=` declares and initializes, `=` assigns, and an assignment to an undeclared name does not compile.
- Several variables can change in one line, so values swap without a temporary: `a, b = b, a`.
- Function arguments are immutable by default, even when references are passed; mutable args are marked on the call too: `fn multiply_by_2(mut arr []int)` is called as `multiply_by_2(mut nums)`. Use `.clone()` for a mutable copy of an immutable array.
- Method receivers: `fn (mut u User) register() { u.is_registered = true }` called on a `mut user`.
- Struct fields are private and immutable unless declared under `mut:` (or `pub mut:`).
- V does not allow modification of arguments of primitive types (such as integers); only more complex types such as arrays and maps may be modified. The docs prefer returning values (`user = register(user)`) and reserve `mut` arguments for performance-critical code.
- A mutable reference needs a mutable variable: `mut c := &fc` works only when `fc` is `mut`.

Verify: remove `mut` and confirm the compiler rejects the assignment.

## Checked

Date: 2026-11-02. Confirmed in the V documentation (doc/docs.md, "Variables", "Mutable variables", "Immutable function args by default", "Mutable arguments", "Heap structs", "Access modifiers"). Removed as not stated there: `<<` on a `mut` array, the unused-`mut` notice, error text for non-`mut` parameters, the deep-freeze remark for `&T` fields.

Method: documentation only; no commands were run.
