---
id: computing-software.software-engineering.v-lang.v-generic-functions
name: v-generic-functions
category: computing-software
field: software-engineering
product: v-lang
tags: [v-generic-functions, generics, generic function, t, type parameter, monomorphisation, v-lang]
level: practitioner
status: docs-checked
description: "Write functions with [T] type parameters, rely on inference or explicit type arguments, use constraints, and branch with $if T is."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generic functions

Goal: reuse logic across types.

- Declare type parameters in square brackets: `fn compare[T](a T, b T) int { ... }`. V generates a version for every type it is used with. Call with inference, `compare(1, 0)`, or explicitly, `new_repo[User](db)`.
- A generic function can be specialized as a value: `f := identity[int]`.
- Currently a generic definition must declare its type parameters. A type parameter that does not appear in the parameters, return type or constraints needs an explicit type argument.
- Constraints name what type arguments must be after the parameter: an interface (`fn longest[T Named](a T, b T) T`), a sum type (`type Number = int | f64`, `fn half[T Number](x T) T`), or a struct. Calls are checked where they are written and the body gets what the constraint provides.
- Branch on the concrete type with `$if T is f64 { ... } $else { ... }`; in the `$else` branch `T` is the rest of the set.
- `T.name` gives the type name (used in the docs for table names).
- Variadic generics: `fn accept[T](items ...T)` infers `T` from `accept(1, 2)` or `accept(...[1, 2])`.
- Generic methods use the receiver's parameter: `fn (r Repo[T]) find_by_id(id int) ?T`; calls can omit `[T]` because it is inferred from the receiver.

Verify: call a generic function with int, string and f64 arguments, as in the docs `compare` example.

## Checked

Date: 2026-11-03. Confirmed in the V documentation (doc/docs.md, "Generics" and "Constraints"). Removed or corrected: the claim "no explicit trait bounds" (the docs describe constraints), `pair[K, V]` example, the 2022 syntax-change note, "inference fails when T appears only in the return type" (replaced by the documented rule about parameters absent from parameters, return type and constraints), and the monomorphisation overhead claim.

Method: documentation only; no commands were run.
