---
id: computing-software.software-engineering.julia.jl-performance-tips
name: jl-performance-tips
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-performance, performance-tips]
level: advanced
status: docs-checked
description: "Remove allocations, preallocate outputs, use in-place ops and avoid abstract containers."
sources: ["https://docs.julialang.org/en/v1/manual/performance-tips/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Allocation, preallocation and in-place operations
- Measure first: `@time` (run twice, the first includes compilation); BenchmarkTools.jl is the package the manual points to for more careful timing.
- Preallocate with `zeros`, `similar`, and use `mul!`, `ldiv!`, `.=`, `map!`; `@views` for slices.
- Avoid `Vector{Any}`/`Vector{Real}`; use concrete element types.
- `@inbounds` removes bounds checks (only after verifying); `@simd` hints vectorisation; `@fastmath` changes floating-point semantics.
- Column-major order: inner loop over the first index.
Verify: `@allocated` is zero for the hot function.

## Checked

2026-11-03. Confirmed against: Performance Tips (`@time` run twice, BenchmarkTools mention, preallocation, `similar`, in-place `mul!`/`ldiv!`/`map!`, `.=`, `@views`, abstract containers, `@inbounds`, `@simd`, `@fastmath`, column-major order, `@allocated`). Removed: `@btime`/`@benchmark` usage and the `$` interpolation claim (only the package mention is on the page); the description no longer mentions fused broadcast.
Method: documentation only; no commands were run.
