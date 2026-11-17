---
id: computing-software.computer-graphics-engineering.graphics-math.deterministic-floating-point
name: deterministic-floating-point
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, numerical-robustness, deterministic-float, lockstep, cross-platform, fma, reproducibility]
level: advanced
status: draft
description: "Get bit-identical floating point across machines for lockstep games and replays: compiler flags, x87/FMA contraction, transcendentals, SIMD/thread order, testing."
sources: ["https://gafferongames.com/post/floating_point_determinism/", "https://randomascii.wordpress.com/2013/07/16/floating-point-determinism/", "https://box2d.org/posts/2024/08/determinism/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Deterministic floating point across platforms

IEEE 754 basic operations (+, -, *, /, sqrt) are correctly rounded, so identical sequences of
operations on identical inputs give identical bits. Non-determinism comes from **different
sequences**.

## Sources of divergence
- **FMA contraction**: `a*b + c` fused on one compiler/CPU (ARM, AVX2 builds) and not on another.
  Disable with `-ffp-contract=off` (GCC/Clang) or `/fp:precise` + no `/arch` FMA auto-generation;
  write explicit `fma()` where you want it.
- **Fast-math**: reassociation, reciprocal approximations, flush-to-zero. Use `-fno-fast-math`,
  `/fp:precise` or `/fp:strict`.
- **x87** 80-bit intermediates (32-bit x86): use SSE2 (`-mfpmath=sse -msse2`); a non-issue on x64.
- **Transcendentals** (`sin`, `exp`, `pow`, `atan2`) differ between libm implementations and versions.
  Ship your own implementations (polynomial approximations using basic operations) or use a
  deterministic library (e.g. streflop-style, or Box2D v3's own `b2Atan2`/`b2ComputeCosSin`).
- **Order of operations**: parallel reductions, unordered containers, multithreaded solvers, SIMD
  width differences (4 vs 8 lane horizontal sums). Fix the reduction order and iterate containers in
  a defined order.
- **Uninitialised data, different input ordering** (e.g. physics bodies added in a different order).
- GPU computation: assume non-deterministic across vendors and drivers; keep simulation on CPU.

## Strategies
1. Fixed-point arithmetic for the simulation (fully deterministic, see fixed-point skill) - common in
   RTS lockstep.
2. Float with strict flags, custom math functions, single-threaded or order-stable parallelism, same
   compiler and flags on all platforms where possible.
3. Server-authoritative state sync instead of lockstep when determinism cannot be guaranteed.

## Testing
- Run the same replay on every target platform/compiler and hash the full simulation state every
  frame (e.g. xxHash of all positions/velocities as raw bits). Report the first diverging frame and
  field.
- Run in CI on every change; determinism regressions are easy to introduce (a new `std::sin`).

## Verify
Bit-identical state hashes after 10,000+ frames across Windows/Linux/macOS, x64/ARM64 builds.
