---
id: computing-software.software-engineering.julia.jl-parametric-types-where-bounds
name: jl-parametric-types-where-bounds
category: computing-software
field: software-engineering
product: julia
tags: [julia, parametric-types-where-bounds]
level: advanced
status: docs-checked
description: "Declare parametric structs and abstract types, subtype bounds with <:, and Type{T} dispatch."
sources: ["https://docs.julialang.org/en/v1/manual/types/", "https://docs.julialang.org/en/v1/manual/faq/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parametric types
- `struct Point{T<:Real}; x::T; y::T; end`; `Point{Int}` is concrete, `Point` alone is a UnionAll.
- Invariance: `Vector{Int}` is not a subtype of `Vector{Number}`; write `Vector{<:Number}`.
- `Type{T}` and `::Type{T}` arguments dispatch on a type value; `Val{N}` dispatches on constants.
- Check with `isconcretetype`, `<:`, `typeof`, `supertype`.
Verify: `Point{Int} <: Point{<:Real}` is true.

## Checked

2026-11-02. Confirmed against: Manual Types and FAQ pages: parametric types, invariance, UnionAll, Type{T}, Val. Removed: nothing.
Method: documentation only; no commands were run.
