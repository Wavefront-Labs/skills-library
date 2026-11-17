---
id: computing-software.software-engineering.v-lang.v-type-aliases-and-casting-rules
name: v-type-aliases-and-casting-rules
category: computing-software
field: software-engineering
product: v-lang
tags: [v-type-aliases-and-casting-rules, type-alias, type-declaration, casting, sum-types, function-types, v-lang]
level: practitioner
status: docs-checked
description: "Declare a type alias with type NewType = ExistingType, initialise numeric aliases with ordinary conversions and know what aliases inherit."
sources:
  - https://raw.githubusercontent.com/vlang/v/master/doc/docs.md
  - https://docs.vlang.io/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Type aliases and explicit casting

Goal: name domain types.

- `type NewType = ExistingType` declares an alias. The docs call it a special case of a sum type declaration.
- Numeric aliases use ordinary conversions for initialisation: `type Decimal = f64` then `amount := Decimal(0.0)`.
- Aliases inherit custom `.str()` methods, including after unwrapping an optional alias value.
- Methods declared on a fixed-array alias keep that alias receiver, even when the name matches a builtin array method.
- Enum aliases stored in struct fields support `.str()` and interpolation using the enum value name.
- Function signatures can be named the same way: `type Filter = fn (string) string` (see v-type-definitions-and-function-types).
- Bare integer literals need an explicit cast to wide types such as `u128(...)`.

Gotchas:
- This page covers declaration and initialisation only; it does not state how aliases and their base types convert
  in function arguments. Test the conversion you rely on against your compiler version.

Verify: `type Decimal = f64`, `amount := Decimal(0.0)`, `println(amount)` compiles and runs.

## Checked

Read the Type aliases, Function Types and integer-literal sections of the V documentation (doc/docs.md from the vlang/v repository, the source of docs.vlang.io). The draft's claims that an alias is a distinct, non-interchangeable type, that `int(id)` conversion is required, that `as` is for sum types only, and the module rule for alias methods are not stated on the page and were removed. Tags previously contained spaces and were fixed.

Method: docs-only read of cited pages, 2026-11-08
