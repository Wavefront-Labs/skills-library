---
id: computing-software.software-engineering.julia.jl-dict-set-operations
name: jl-dict-set-operations
category: computing-software
field: software-engineering
product: julia
tags: [julia, dict-set-operations]
level: practitioner
status: docs-checked
description: "Use Dict, Set, get!, haskey, merge and ordered alternatives in Julia."
sources: ["https://docs.julialang.org/en/v1/manual/noteworthy-differences/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dict and Set
- `d = Dict("a"=>1)`; `get(d,"b",0)`, `get!(d,"b",0)` (inserts), `haskey`, `delete!`, `pairs`, `keys`, `values`.
- `merge(d1,d2)` creates a new Dict (later wins); `merge!` mutates; `mergewith(+, d1, d2)` combines values.
- A `Dict` is not ordered.
- `Set`, `union`, `intersect`, `setdiff`, `in`.
Verify: `mergewith(+, Dict(:a=>1), Dict(:a=>2))` is `Dict(:a=>3)`.

## Checked

2026-11-02. Confirmed against: Base collections docs (Dict, get!, haskey, delete!, merge, merge!, mergewith, Set operations) and manual Noteworthy Differences (Dict is not ordered). Removed: the OrderedCollections suggestion and the mutable-key rule.
Method: documentation only; no commands were run.
