---
id: computing-software.software-engineering.julia.jl-constructors-inner-outer
name: jl-constructors-inner-outer
category: computing-software
field: software-engineering
product: julia
tags: [julia, constructors-inner-outer]
level: advanced
status: docs-checked
description: "Write Julia outer constructors for convenience and inner constructors to enforce invariants."
sources: ["https://docs.julialang.org/en/v1/manual/constructors/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Constructors
- Outer: `Point(x) = Point(x, 0)` added after the type; inner constructors live inside the struct and suppress the default ones.
- Inner: `Positive(x) = x > 0 ? new(x) : throw(ArgumentError("must be positive"))`; `new` only works inside.
- For parametric types use `Point{T}(x, y) where T`.
Verify: constructing with an invalid argument throws.

## Checked

2026-11-02. Confirmed against: Manual Constructors page: outer and inner constructors, new, default constructors suppressed by an inner constructor, parametric constructors. Removed: the show, == and hash advice.
Method: documentation only; no commands were run.
