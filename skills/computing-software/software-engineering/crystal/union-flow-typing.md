---
id: computing-software.software-engineering.crystal.union-flow-typing
name: union-flow-typing
category: computing-software
field: software-engineering
product: crystal
tags: [union-flow-typing, union-types, narrowing, as-cast, is-a, casting, not-nil, union-narrowing, crystal]
level: practitioner
status: draft
description: "Narrow a union with is_a?, nil?, case/when, responds_to?, as casts and not_nil! to call member-specific methods."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Narrowing unions

Goal: turn a union into a single type safely.

- `if x.is_a?(String)` narrows `x` inside the branch; `else` gets the remaining types.
- `x.as(String)` casts or raises `TypeCastError`; `x.as?(String)` returns `String?`.
- `case x when String ... when Int32 ...` narrows per branch.
- `x.not_nil!` removes Nil or raises.

Gotchas:
- Narrowing works on local variables, not on method calls or instance variables (copy to a local first or use `if (v = @v)`).
- Narrowing is lost if the variable is captured and reassigned in a closure.
- `as` on a union that cannot hold that type is a compile error.

Verify: spec with each variant, asserting TypeCastError for the bad cast.
