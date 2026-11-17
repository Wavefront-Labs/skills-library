---
id: computing-software.software-engineering.julia.jl-random-and-statistics
name: jl-random-and-statistics
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-numerics, random-and-statistics]
level: practitioner
status: docs-checked
description: "Seed RNGs, draw samples with Random and compute summary statistics with the Statistics stdlib."
sources: ["https://docs.julialang.org/en/v1/stdlib/Random/", "https://docs.julialang.org/en/v1/stdlib/Statistics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Random numbers and Statistics
- `using Random; Random.seed!(42); rand(3)`, `randn`, `rand(1:6, 10)`, `shuffle`, `randperm`; the default RNG stream may change between Julia versions.
- Pass an explicit `rng = MersenneTwister(1)`; the default RNG is thread-safe, and for reproducible parallel code give each task or thread its own RNG object.
- `Statistics`: `mean`, `median`, `std`, `var`, `cor`, `quantile`.
Verify: reseeding reproduces the draws.

## Checked

2026-11-03. Confirmed against: stdlib Random (functions above, `MersenneTwister`, stream stability note, task-local thread-safe default RNG) and stdlib Statistics. Removed: StableRNG, StatsBase.sample and Distributions.jl (`Normal`, `pdf`, `cdf`), which are third-party and not on the pages read; the "one RNG per task" rule is reworded to the docs.
Method: documentation only; no commands were run.
