---
id: computing-software.software-engineering.crystal.method-return-types
name: method-return-types
category: computing-software
field: software-engineering
product: crystal
tags: [method-return-types, types-and-methods, return-type, noreturn, nil-return, type-annotation, void, crystal]
level: practitioner
status: draft
description: "Annotate return types, use NoReturn and Nil, and understand how the compiler infers and checks method return types."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Return types and method type annotations

Goal: use return annotations deliberately.

- `def foo : Int32` checks the returned value's type at compile time.
- `: Nil` discards the value, handy for `to_s(io)`.
- `NoReturn` is the type of `raise`, `exit`, infinite loops; it vanishes from unions, so `x = cond ? 1 : raise "e"` is Int32.
- `: self` returns the receiver type, helpful for chaining under inheritance.
- Without an annotation the return type is inferred from the body, per call-site argument types.

Gotchas:
- Annotating a wider type than the body (for example `: Int32 | String`) is fine; a mismatch is an error.
- Recursive methods may need an annotation when inference cannot terminate.
- Abstract defs should carry annotations to document the contract.

Verify: return a String from an Int32-annotated method and expect an `expected this method to return Int32` style error.
