---
id: computing-software.software-engineering.julia.jl-type-promotion-conversion
name: jl-type-promotion-conversion
category: computing-software
field: software-engineering
product: julia
tags: [julia, type-promotion-conversion]
level: practitioner
status: docs-checked
description: "Control Julia numeric mixing with promote, convert, promote_rule and the Int overflow wraparound behaviour."
sources: ["https://docs.julialang.org/en/v1/manual/conversion-and-promotion/", "https://docs.julialang.org/en/v1/manual/integers-and-floating-point-numbers/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Promotion and conversion
- `promote(1, 2.5)` yields `(1.0, 2.5)`; arithmetic operators call `promote`. Define `Base.promote_rule(::Type{A}, ::Type{B})` and `Base.convert` for custom numeric types.
- `convert(Int, 3.0)` works, `convert(Int, 3.5)` throws `InexactError`; use `round(Int, x)`, `floor`, `trunc`.
- Integers wrap on overflow (`typemax(Int) + 1 == typemin(Int)`); use `BigInt` when needed.
Verify: `typeof(promote(1, 2f0)...)` is `Float32`.

## Checked

2026-11-02. Confirmed against: Manual Conversion and Promotion and Integers and Floating-Point Numbers pages (promotion, InexactError, overflow wrap-around). Removed: the Base.checked_add mention.
Method: documentation only; no commands were run.
