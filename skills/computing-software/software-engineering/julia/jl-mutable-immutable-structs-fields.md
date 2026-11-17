---
id: computing-software.software-engineering.julia.jl-mutable-immutable-structs-fields
name: jl-mutable-immutable-structs-fields
category: computing-software
field: software-engineering
product: julia
tags: [julia, mutable-immutable-structs-fields]
level: practitioner
status: docs-checked
description: "Pick struct vs mutable struct, annotate concrete field types, and use const fields (1.8+)."
sources: ["https://docs.julialang.org/en/v1/manual/types/", "https://docs.julialang.org/en/v1/manual/performance-tips/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# struct vs mutable struct
- `struct` is immutable and often stack-allocated/inlined; `mutable struct` has identity and heap allocation.
- Abstract field types (`x::Real`, untyped `x`) force boxing and dynamic dispatch; use concrete types or parametrise: `struct S{T<:Real}; x::T; end`.
- `mutable struct S; const id::Int; value::Float64; end` (requires Julia 1.8) freezes selected fields.
Verify: `isbitstype(S)` and `@allocated` on a loop.

## Checked

2026-11-02. Confirmed against: Manual Types page (immutable and mutable composite types, const fields since Julia 1.8) and Performance Tips (abstract fields). Removed: the Setfield.jl and Accessors.jl advice.
Method: documentation only; no commands were run.
