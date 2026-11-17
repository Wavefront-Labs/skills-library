---
id: computing-software.software-engineering.concurrency.simd-and-auto-vectorisation
name: simd-and-auto-vectorisation
category: computing-software
field: software-engineering
product: concurrency
tags: [concurrency, optimisation, simd, vectorization, auto-vectorization, avx2, neon]
level: practitioner
status: draft
description: "Use SIMD for data-parallel hot loops: help compilers auto-vectorise, read vectorisation reports, use portable SIMD APIs (Vector<T>, std::simd, Java Vector API) and dispatch by CPU."
sources:
  - https://llvm.org/docs/Vectorizers.html
  - https://gcc.gnu.org/projects/tree-ssa/vectorization.html
  - https://learn.microsoft.com/en-us/dotnet/standard/simd
  - https://openjdk.org/jeps/489
  - https://doc.rust-lang.org/std/simd/index.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SIMD and auto-vectorisation

SIMD instructions process several values per instruction: SSE (128-bit), AVX2 (256-bit), AVX-512 on x86; NEON (128-bit) and SVE on ARM. Eight floats per AVX2 instruction can mean big speedups on loops over arrays - when memory bandwidth is not the limit.

## 1. Let the compiler do it (auto-vectorisation)
Loops vectorise when they are simple: countable trip count, contiguous arrays, no loop-carried dependencies, no calls that cannot be inlined, no aliasing doubts.
```c
// vectorises: independent iterations, restrict promises no aliasing
void saxpy(size_t n, float a, const float *restrict x, float *restrict y) {
    for (size_t i = 0; i < n; i++) y[i] = a * x[i] + y[i];
}
```
Blockers: pointer aliasing (use `restrict`/`__restrict`, Rust slices give it for free), branches in the body (rewrite as branchless select), early exits, non-unit strides (AoS layouts - switch to SoA), floating-point reductions (strict IEEE ordering forbids reassociation; `-ffast-math`/`-fassociative-math` allows it at the cost of exact results).

Compile for the target CPU: `-O3 -march=x86-64-v3` (AVX2) or `-march=native` for local-only builds; Rust `RUSTFLAGS="-C target-cpu=x86-64-v3"`; .NET and JVM JITs use the host CPU automatically.

## 2. Check what happened
- Clang: `-Rpass=loop-vectorize -Rpass-missed=loop-vectorize -Rpass-analysis=loop-vectorize`.
- GCC: `-fopt-info-vec-optimized -fopt-info-vec-missed`.
- Compiler Explorer (godbolt.org) to read the assembly: look for `ymm`/`zmm` registers (AVX) or `v`-prefixed NEON ops and packed instructions (`vfmadd...ps`).
- JVM: `-XX:+UnlockDiagnosticVMOptions -XX:+PrintAssembly` (with hsdis) or JITWatch.

## 3. Portable explicit SIMD
- .NET: `Vector<T>` (hardware width) and `Vector128/256/512<T>`, plus `System.Runtime.Intrinsics` for specific instructions; many BCL methods (`Span.IndexOf`, `Sum` in .NET 8) are already vectorised.
- Java: Vector API (`jdk.incubator.vector`, still incubating - needs `--add-modules jdk.incubator.vector`).
- Rust: `std::simd` (nightly portable SIMD) or crates `wide`, `pulp`; `std::arch` intrinsics for specific targets.
- C++: `std::experimental::simd` (C++26 `std::simd`), Highway (Google), xsimd, or intrinsics (`immintrin.h`, `arm_neon.h`).
- Python: NumPy/Polars already use SIMD internally - vectorise at the array level instead of writing loops.

## Runtime dispatch
Shipping one binary for many CPUs: detect features at runtime and pick an implementation (GCC/Clang function multiversioning `__attribute__((target_clones("avx2","default")))`, Rust `is_x86_feature_detected!`, .NET `Avx2.IsSupported`, Highway dynamic dispatch). Always keep a scalar fallback and test it.

## Gotchas
- Memory-bound loops gain little - check arithmetic intensity first (roofline thinking).
- AVX-512 can lower clock frequency on some older Intel CPUs.
- Handle the tail (n not a multiple of the vector width) and alignment.
- Results of vectorised float reductions differ slightly from scalar order; tests need tolerances.

## Verify
- [ ] Vectorisation report or assembly confirms vector instructions in the hot loop.
- [ ] Benchmark at realistic sizes shows the gain; scalar and SIMD paths produce equal results (within tolerance) in tests.
