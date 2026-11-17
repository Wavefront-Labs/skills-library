---
id: computing-software.software-engineering.julia.jl-comprehensions-generators
name: jl-comprehensions-generators
category: computing-software
field: software-engineering
product: julia
tags: [julia, comprehensions-generators]
level: practitioner
status: docs-checked
description: "Build arrays with comprehensions, generators and filtered/multi-dimensional forms in Julia."
sources: ["https://docs.julialang.org/en/v1/manual/arrays/", "https://docs.julialang.org/en/v1/manual/performance-tips/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Comprehensions
- `[x^2 for x in 1:5 if isodd(x)]`; `[i*j for i in 1:3, j in 1:3]` makes a 3x3 matrix.
- Parenthesised generators `(x^2 for x in 1:5)` are lazy: `sum(x^2 for x in 1:10^6)` avoids allocating.
- `Dict(k=>v for ...)`; `collect(gen)` materialises; `Iterators.product/flatten/partition` for more.
Verify: compare `@allocated` of `sum` over a generator with `sum` over the collected array.

## Checked

2026-11-02. Confirmed against: Manual Arrays page (comprehensions, generator expressions) and Base iterators docs (Iterators.product, flatten, partition). Removed: the near-zero allocation figure.
Method: documentation only; no commands were run.
