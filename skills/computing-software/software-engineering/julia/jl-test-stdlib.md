---
id: computing-software.software-engineering.julia.jl-test-stdlib
name: jl-test-stdlib
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-testing, test-stdlib]
level: practitioner
status: docs-checked
description: "Write @testset blocks with @test, @test_throws, @test_broken, @inferred and approximate comparison."
sources: ["https://docs.julialang.org/en/v1/stdlib/Test/", "https://docs.julialang.org/en/v1/stdlib/Random/", "https://pkgdocs.julialang.org/v1/repl/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Test.jl, testsets and approximate comparison
- `@testset "name" begin @test f(1) == 2; @test_throws DomainError f(-1); @test x ≈ y atol = 1e-8 end`.
- `@test_broken` marks known failures; `@inferred` checks type stability; `@test_logs` checks logging.
- Seed randomness with `using Random; Random.seed!(1)`; the default RNG stream may change between Julia versions.
- Code coverage: `pkg> test --coverage`.
Verify: break the function and confirm the testset fails.

## Checked

2026-11-03. Confirmed against: stdlib Test (macros above, `atol`), stdlib Random (`seed!`, stream not stable across versions) and the Pkg REPL page (`test --coverage`). Removed: StableRNGs.jl, Coverage.jl/Codecov and Aqua.jl claims (third-party, not on the pages read).
Method: documentation only; no commands were run.
