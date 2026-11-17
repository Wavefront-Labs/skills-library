---
id: computing-software.software-engineering.julia.jl-array-indexing-broadcast
name: jl-array-indexing-broadcast
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-collections, array-indexing-broadcast]
level: practitioner
status: docs-checked
description: "Index arrays correctly, use views to avoid copies and broadcast with the dot syntax."
sources: ["https://docs.julialang.org/en/v1/manual/arrays/", "https://docs.julialang.org/en/v1/manual/performance-tips/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# 1-based indexing, views and broadcasting
- Arrays are 1-based and column-major; loop the first index innermost. Use `eachindex(A)` or `axes(A)` for generic code.
- Slices copy; `@view A[:, 1]` or `@views` avoids it.
- Broadcast with dot calls: `f.(x)`, `x .+ y`, `@. a + b * c`; fused dotted expressions avoid temporary arrays.
- `push!`, `append!`, `pop!`, `splice!` mutate vectors.
- Functions ending with `!` mutate their first argument by convention.
Verify: `@allocated` shows no copy for a view-based loop.

## Checked

2026-11-02. Confirmed against: Manual pages Arrays and Performance Tips: column-major order, views for slices, dot fusion, eachindex and axes. Removed: the OffsetArrays aside and the `A[:]` versus `vec(A)` memory-sharing claim.
Method: documentation only; no commands were run.
