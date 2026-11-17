---
id: computing-software.software-engineering.julia.jl-linear-algebra-stdlib
name: jl-linear-algebra-stdlib
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-numerics, linear-algebra-stdlib]
level: advanced
status: docs-checked
description: "Solve systems with factorizations, use mul! and structured matrices and control BLAS threads."
sources: ["https://docs.julialang.org/en/v1/stdlib/LinearAlgebra/", "https://docs.julialang.org/en/v1/manual/performance-tips/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LinearAlgebra, factorizations and BLAS threads
- `using LinearAlgebra`; `A \ b` picks a suitable factorisation; `lu(A)`, `qr(A)`, `cholesky(A)` return factorisation objects that can be used with `\`.
- Structured types `Diagonal`, `Symmetric`, `Tridiagonal`, `UpperTriangular` dispatch to faster algorithms.
- `mul!(C, A, B)` is in-place; `I` is the lazy identity (`UniformScaling`); `norm`, `det`, `eigen`, `svd`, `cond`.
- `BLAS.set_num_threads(n)` to avoid oversubscription when also using Julia threads.
Verify: `norm(A*x - b)` small.

## Checked

2026-11-03. Confirmed against: stdlib LinearAlgebra (polyalgorithm `\`, factorisations, structured types, `mul!`, `UniformScaling`, `BLAS.set_num_threads`) and Performance Tips (BLAS/thread oversubscription). Removed: the "Sparse (SparseArrays)" entry from the structured-type list and the claim that `F \ b` reuses work beyond what the factorisation objects document.
Method: documentation only; no commands were run.
