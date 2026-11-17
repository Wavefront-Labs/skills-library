---
id: computing-software.software-engineering.julia.jl-structs-constructors
name: jl-structs-constructors
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-structs, structs-constructors]
level: practitioner
status: docs-checked
description: "Choose immutable versus mutable structs and write inner and outer constructors with validation."
sources: ["https://docs.julialang.org/en/v1/manual/types/", "https://docs.julialang.org/en/v1/manual/constructors/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# struct, mutable struct and constructors
- `struct` is immutable (fields cannot be reassigned) and can be stack-allocated; `mutable struct` allows mutation.
- Inner constructors enforce invariants: `struct P; x::Int; P(x) = x < 0 ? error("negative") : new(x); end` disables the default constructor.
- `Base.@kwdef struct Cfg; n::Int = 1; name::String = "a"; end` gives keyword constructors with defaults.
- Redefining a struct needs a restart (or Revise cannot change layouts in a session).
Verify: construct with an invalid value and see the error.

## Checked

2026-11-02. Confirmed against: Manual Types and Constructors pages. Removed: nothing.
Method: documentation only; no commands were run.
