---
id: computing-software.software-engineering.julia.jl-enums-constants
name: jl-enums-constants
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-enums-consts, enums-constants]
level: practitioner
status: docs-checked
description: "Define enumerations with @enum, constants with const and know that redefining a const may cause recompilation."
sources: ["https://docs.julialang.org/en/v1/base/base/", "https://docs.julialang.org/en/v1/manual/variables-and-scoping/", "https://docs.julialang.org/en/v1/manual/performance-tips/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# @enum and const
- `@enum Color red green blue` creates a type `Color` with `Int32` values by default; `instances(Color)` lists members and `Symbol(red)` gives the name.
- Add explicit values: `@enum Fruit apple = 1 orange = 2`.
- `const N = 10` fixes the binding (not the value's mutability); const globals are fast. Reassigning a const name without `const` is an error; redefining it with `const` is allowed but may cause recompilation and was poorly supported before Julia 1.12.
Verify: `instances(Color)` returns all members.

## Checked

2026-11-03. Confirmed against: Base docs (`@enum`, `instances`, `const`), Manual Variables and Scoping (const binds the name only, redefinition) and Performance Tips (const globals). Real error fixed: the draft said redefining a const to a different type is an error and to the same type warns; the docs say redefinition is allowed and may cause recompilation. Removed: the bit-flag `|` claim, the `Color(1)` conversion line and the "no exhaustive match" note (not on the pages read).
Method: documentation only; no commands were run.
