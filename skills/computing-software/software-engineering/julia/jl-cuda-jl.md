---
id: computing-software.software-engineering.julia.jl-cuda-jl
name: jl-cuda-jl
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-gpu, cuda-jl]
level: advanced
status: draft
description: "Run array code on NVIDIA GPUs with CUDA.jl, avoid scalar indexing and write simple kernels."
sources: ["https://docs.julialang.org/en/v1/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CUDA.jl arrays and kernels
- `using CUDA; x = CuArray(rand(Float32, 1000))`; broadcast and `sum` run on the device; `Array(x)` copies back.
- Disable scalar indexing with `CUDA.allowscalar(false)` to catch slow loops.
- Kernels: `@cuda threads = 256 blocks = cld(n, 256) kernel(args...)`, with `threadIdx().x`, `blockIdx().x`.
- Use `Float32`; `CUDA.@sync` for timing; `CUDA.versioninfo()` diagnoses drivers.
Verify: compare GPU and CPU results with `isapprox`.
