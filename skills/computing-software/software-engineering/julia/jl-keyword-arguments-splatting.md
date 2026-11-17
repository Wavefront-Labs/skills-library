---
id: computing-software.software-engineering.julia.jl-keyword-arguments-splatting
name: jl-keyword-arguments-splatting
category: computing-software
field: software-engineering
product: julia
tags: [julia, keyword-arguments-splatting]
level: practitioner
status: docs-checked
description: "Write Julia functions with positional defaults, keyword args after a semicolon, varargs and splat."
sources: ["https://docs.julialang.org/en/v1/manual/functions/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Arguments
- `f(a, b=2; verbose=false, kw...)`; call `f(1; verbose=true)`. Keyword args do not participate in dispatch.
- Varargs `g(xs...)`, splatting `g(v...)`, `g(; d...)` for NamedTuples/Dicts of symbols.
- `Base.@kwdef struct Opts; n::Int = 3; end` creates keyword constructors.
- Short form `f(x) = x^2`, anonymous `x -> x^2`, composition `f ∘ g`, pipe `x |> f`.
Verify: `f(1; verbose=true)` toggles behaviour.

## Checked

2026-11-02. Confirmed against: Manual Functions page: keyword arguments, varargs, splatting, anonymous functions, composition and pipe. Removed: nothing.
Method: documentation only; no commands were run.
