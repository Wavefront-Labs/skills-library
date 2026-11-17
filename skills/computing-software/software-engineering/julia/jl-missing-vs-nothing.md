---
id: computing-software.software-engineering.julia.jl-missing-vs-nothing
name: jl-missing-vs-nothing
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-missing-nothing, missing-vs-nothing]
level: practitioner
status: docs-checked
description: "Distinguish missing (data absence, propagates) from nothing (no value) and handle both."
sources: ["https://docs.julialang.org/en/v1/manual/missing/", "https://docs.julialang.org/en/v1/base/base/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# missing, nothing and Union types
- `missing` propagates through standard math operators (`missing + 1` is `missing`); `if missing` throws a `TypeError` ("non-boolean (Missing) used in boolean context").
- Use `ismissing(x)` to test; `coalesce(x, 0)` returns the first non-missing argument; `skipmissing(xs)` iterates skipping missing values.
- `something(x, default)` returns the first value that is not `nothing`; `isnothing(x)` tests `x === nothing`.
- `Array{Union{Missing,T}}` stores values efficiently in an `Array{T}` plus a type tag array.
Verify: `sum(skipmissing(v))` on data containing `missing`.

## Checked

Date: 2026-11-02. Confirmed on Julia manual 'Missing Values' and Base docs (TypeError on `if missing`, propagation, skipmissing, coalesce, ismissing, something, isnothing, Union array storage). Removed as not confirmed: union splitting remark and the findfirst/match examples.

Method: documentation only; no commands were run.
