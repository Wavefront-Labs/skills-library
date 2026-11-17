---
id: computing-software.software-engineering.julia.jl-autodiff-flux
name: jl-autodiff-flux
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-autodiff, autodiff-flux]
level: advanced
status: draft
description: "Differentiate Julia code with ForwardDiff or Zygote and train small models with Flux."
sources: ["https://docs.julialang.org/en/v1/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ForwardDiff, Zygote and Flux
- `ForwardDiff.gradient(f, x)` is forward-mode: good for few inputs; Zygote `gradient(f, x)` reverse-mode: good for many inputs but struggles with mutation.
- Flux: `model = Chain(Dense(2 => 8, relu), Dense(8 => 1))`; `Flux.setup(Adam(0.01), model)` and `Flux.train!`; move to GPU with `gpu` or CUDA.jl arrays.
- Type-unstable or mutating code breaks reverse-mode AD; check with finite differences.
Verify: `isapprox(grad, finite_diff)`.
