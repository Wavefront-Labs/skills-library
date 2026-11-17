---
id: computing-software.software-engineering.julia.jl-dict-set-tuples
name: jl-dict-set-tuples
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-collections, dict-set-tuples]
level: practitioner
status: gated
description: "Select the right collection and use getkey, get!, haskey, merge and immutable tuples."
sources: ["https://docs.julialang.org/en/v1/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dict, Set, Tuple and NamedTuple
- `d = Dict("a" => 1)`; `get(d, k, default)`, `get!(d, k) do ... end`, `haskey(d, k)`, `delete!(d, k)`; `Dict` iteration order is not guaranteed (use `OrderedCollections.OrderedDict`). (gated: unconfirmed, source is paywalled or blocked)
- Mutable keys hashed once can break the dict when mutated; use immutable keys.
- `Tuple` is immutable and fixed-length; `NamedTuple` is `(a = 1, b = 2)` with `nt.a`.
- Comprehensions `[f(x) for x in xs if p(x)]`, generators `(f(x) for x in xs)` are lazy.
Verify: `typeof(d)` shows concrete key and value types.

## Checked

Date: 2026-11-02. Gated: Julia manual (dicts) was not fetched.

Method: documentation only; no commands were run.
