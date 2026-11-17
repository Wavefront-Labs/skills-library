---
id: computing-software.software-engineering.v-lang.v-generic-constraints-and-comptime-checks
name: v-generic-constraints-and-comptime-checks
category: computing-software
field: software-engineering
product: v-lang
tags: [v-generic-constraints-and-comptime-checks, generics, constraints, comptime, compile-time-types, type-name, v-lang]
level: advanced
status: docs-checked
description: "Constrain V generic type parameters with interfaces, sum types or structs, and specialise with $if T is, T.name and the $int/$array/$struct compile-time types."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generic constraints and comptime type checks

Goal: specialise generic code without runtime reflection.

- A type parameter can name what its type arguments must be after it: an interface (which the argument implements), a sum type or an alias of one (whose variants are the allowed types), or a struct (that struct plus structs embedding it).
- Calls are checked against the constraint where written. In the body, a value of the type parameter has what the constraint provides: interface or struct members, or what every variant of the sum type has, operators included.
- Docs example: `fn longest[T Named](a T, b T) T` with `interface Named { name string }`, and `type Number = int | f64` with `fn half[T Number](x T) T`. `longest(1, 2)` is reported at the call because `int` does not implement `Named`.
- In a branch of `$if T is f64 {`, `T` is `f64`, and in its `$else` the rest of the set.
- `T.name` gives the type name (the docs use it to derive a table name in a generic ORM-style function).
- Compile-time types group types for generic checks, for example `$if T is $int`: the docs list `$alias`, `$array`, `$array_dynamic`, `$array_fixed`, `$enum`, `$float`, `$function`, `$int`, `$interface`, `$map`, `$option`, `$shared`, `$struct`, `$sumtype`, `$string`, `$pointer`, `$voidptr`. `$int` matches `int`, `i8`..`i64`, `u8`..`u64`, `uint` and integer literals.
- Walk a struct with `$for field in T.fields { ... }` (see the compile-time reflection skill).
- Type arguments are inferred from runtime arguments, so `compare(1, 0)` needs no `[int]`; a type parameter absent from parameters, return type and constraints needs an explicit type argument.

Gotchas:
- Struct constraints accept finite embedding paths; recursive sum constraints that keep growing their type arguments are rejected.

Verify: instantiate with one type per branch and check the result, as the docs examples do.

## Checked

Confirmed against the "Generics" (including "Constraints") and "Compile time types" sections of doc/docs.md in the vlang/v repository, read 2026-11-08. Removed: `typeof[T]().name` equivalence claim, the zero-cost `@[inline]` helper idea, the "other branches are not type-checked" gotcha, and the docs.vlang.io and modules.vlang.io sources.
Method: docs-only read of cited pages, 2026-11-08
