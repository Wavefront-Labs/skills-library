---
id: computing-software.software-engineering.julia.jl-abstract-concrete-types
name: jl-abstract-concrete-types
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-types, abstract-concrete-types]
level: practitioner
status: docs-checked
description: "Design type hierarchies with abstract types, concrete structs and parametric types and know what subtyping allows."
sources: ["https://docs.julialang.org/en/v1/manual/types/", "https://docs.julialang.org/en/v1/manual/faq/", "https://docs.julialang.org/en/v1/manual/performance-tips/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Abstract, concrete and parametric types
- Only abstract types have subtypes; concrete types are final. `struct Point{T<:Real}; x::T; y::T; end` is parametric.
- `Vector{Int} <: Vector{Real}` is false (parametric types are invariant); write `Vector{<:Real}`.
- Prefer concrete field types or type parameters; an abstract field type such as `x::Real` makes the struct slow.
- Inspect with `supertype(T)`, `subtypes(T)`, `isconcretetype(T)`, `fieldtypes(T)`.
Verify: `@code_warntype` on code that uses the struct shows no `Any`.

## Checked

2026-11-02. Confirmed against: Manual pages Types, FAQ and Performance Tips: abstract and concrete types, parametric invariance, abstract field types, isconcretetype. Removed: nothing.
Method: documentation only; no commands were run.
