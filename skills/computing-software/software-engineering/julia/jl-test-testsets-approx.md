---
id: computing-software.software-engineering.julia.jl-test-testsets-approx
name: jl-test-testsets-approx
category: computing-software
field: software-engineering
product: julia
tags: [julia, test-testsets-approx]
level: practitioner
status: docs-checked
description: "Write Julia tests with @testset, @test, @test_throws, isapprox, and run them with pkg> test."
sources: ["https://docs.julialang.org/en/v1/stdlib/Test/", "https://pkgdocs.julialang.org/v1/repl/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Test.jl
- `using Test; @testset "name" begin @test f(1) == 2; @test_throws ArgumentError f(-1); @test x ≈ y atol=1e-8 end`.
- Nested testsets summarise; `@test_broken` marks known failures; `@inferred f(x)` checks type stability.
- `pkg> test` runs `test/runtests.jl` in a temporary environment; `pkg> test --coverage` collects coverage.
Verify: introduce a failing test to see the summary table.

## Checked

2026-11-03. Confirmed against: stdlib Test and the Pkg REPL page (`test`, `--coverage`, `test/runtests.jl`, temporary environment). Removed: the "confirm flags" hedge, now resolved by the page.
Method: documentation only; no commands were run.
