---
id: computing-software.software-engineering.julia.jl-ranges-sorting
name: jl-ranges-sorting
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-ranges-sorting, ranges-sorting]
level: practitioner
status: docs-checked
description: "Use lazy ranges and sort, sortperm, searchsorted and partialsort with custom ordering."
sources: ["https://docs.julialang.org/en/v1/base/sort/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ranges, sort, sortperm and searching
- `sort(v; by = abs, rev = true)`, `sort!(v)`, `sortperm(v)`, `issorted(v)`; `partialsort(v, 1:3)` accepts a range of ranks.
- `searchsortedfirst(v, x)` requires a sorted vector.
- The sort family uses stable algorithms; since Julia 1.9 the default is guaranteed stable. `InsertionSort` and `MergeSort` are stable; `QuickSort` and `PartialQuickSort(k)` are not.
Verify: `issorted` on the output.

## Checked

Date: 2026-11-02. Confirmed on Julia Sorting and Related Functions docs (signatures, partialsort ranges, default stability since 1.9, algorithm list). Removed as not confirmed: range laziness, LinRange, findall/findfirst/in.

Method: documentation only; no commands were run.
