---
id: computing-software.software-engineering.julia.jl-where-clauses
name: jl-where-clauses
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-where-methods, where-clauses]
level: advanced
status: docs-checked
description: "Write generic methods with where type parameters, Type{T} dispatch and the Val trick."
sources: ["https://docs.julialang.org/en/v1/manual/types/", "https://docs.julialang.org/en/v1/manual/performance-tips/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# where clauses and type parameters in methods
- `f(x::Vector{T}) where {T<:Number} = zeros(T, length(x))` binds `T` from the argument.
- `f(::Type{T}) where {T} = ...` dispatches on a type as a value; `Val{N}()` lifts a value into the type domain for dispatch, but many distinct values cause compile-time blowup.
- Use `T<:AbstractFloat` bounds instead of listing concrete types.
Verify: `methods(f)` shows the where signatures.

## Checked

2026-11-02. Confirmed against: Manual Types page (UnionAll, where, Type{T}, Val) and Performance Tips (Val). Removed: the Aqua.jl claim.
Method: documentation only; no commands were run.
