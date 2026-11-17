---
id: computing-software.software-engineering.d.d-ldc-gdc-extended-asm-and-simd
name: d-ldc-gdc-extended-asm-and-simd
category: computing-software
field: software-engineering
product: d
tags: [d-ldc-gdc-extended-asm-and-simd, inline-asm, ldc-asm, gdc-asm, core-simd, intrinsics, inlineir, vector-types, bitop, llvm-asm, d]
level: sme
status: draft
description: "Portable alternatives to dmd asm: LDC __asm and inlineIR, GDC extended asm with constraints, core.simd vector types and core.bitop intrinsics."
sources:
  - https://dlang.org/spec/spec.html
  - https://dlang.org/phobos/index.html
  - https://dub.pm/
  - https://ddili.org/ders/d.en/index.html
  - https://dlang.org/articles.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LDC/GDC extended asm and core.simd

Goal: reach hardware features across compilers.

- LDC: `import ldc.llvmasm; __asm("cpuid", "={eax},={ebx},={ecx},={edx},{eax}", leaf)` with LLVM constraint strings, or `ldc.intrinsics` (`llvm_ctlz`, `llvm_bswap`, `llvm_fma`); `ldc.simd` helpers, `ldc.attributes` (`@fastmath`, `@target("avx2")`).
- GDC: GCC-style `asm { "add %1, %0" : "=r" (r) : "r" (a) ; }` with outputs/inputs/clobbers (extended asm); `gcc.builtins` exposes `__builtin_*`.
- SIMD: `import core.simd; float4 v = [1,2,3,4]; v += v;` vector types `float4`, `int4`, `double2`, `ubyte16`; check `__traits(compiles, float4)` or `version (D_SIMD)`; use `core.simd.simd!(XMM.ADDPS)`-style intrinsics (dmd) or `std.experimental` / `inteli` (`intel-intrinsics` dub package) for portable SSE/AVX.
- Bit ops: `core.bitop` `popcnt`, `bsf`, `bsr`, `bswap`, `rol`, `ror`, `bt` and `BitArray` (`std.bitmanip`).
- Math: `core.math` (`sqrt`, `fabs`, `rndtol`), `std.math` intrinsic-backed.

Gotchas:
- Constraint strings differ between LDC (LLVM) and GDC (GCC); use `version (LDC)` / `version (GNU)` branches.
- Misaligned vector loads fault; use unaligned load intrinsics.

Verify: run on the target CPU with a known-answer test; compare against scalar loop.
