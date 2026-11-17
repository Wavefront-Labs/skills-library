---
id: computing-software.software-engineering.julia.jl-integer-overflow-float
name: jl-integer-overflow-float
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-types, integer-overflow-float]
level: practitioner
status: docs-checked
description: "Know that Int arithmetic wraps, use big integers or checked ops, and compare floats with isapprox."
sources: ["https://docs.julialang.org/en/v1/manual/integers-and-floating-point-numbers/", "https://docs.julialang.org/en/v1/base/math/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Integer overflow, promotion and floating point
- Int64 arithmetic wraps silently: `typemax(Int64) + 1 == typemin(Int64)`; use `BigInt`, or the `Base.Checked` module for overflow-checked arithmetic.
- `/` on integers returns floating point; `div` truncates, `fld` is the floor and `cld` the ceiling of `x / y`; `rem` has the sign of `x`, `mod` the sign of `y`.
- `isapprox(a, b)` (or `a ≈ b`) uses `atol = 0` and, for floats, `rtol = sqrt(eps)` of the less precise type.
- Underscore digit separators (`10_000`) and hex literals are valid; hex literal size depends on digit count.
Verify: test boundary values with `typemax`.

## Checked

Date: 2026-11-02. Confirmed on Julia manual (integers and floating-point numbers) and Base math docs (wraparound, Base.Checked, div/fld/cld, rem/mod signs, isapprox defaults, underscore and hex literals). Removed as not confirmed: `Base.checked_add` name and `1//3` Rational remark.

Method: documentation only; no commands were run.
