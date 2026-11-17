---
id: computing-software.software-engineering.assembly.avx-vex-ymm
name: avx-vex-ymm
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, avx-vex-ymm, asm-x86-simd]
level: advanced
status: draft
description: "AVX and AVX2 on x86-64: VEX three-operand forms, YMM registers, alignment rules, VZEROUPPER and OS-support detection."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# AVX/AVX2 with VEX encoding and YMM
**Goal:** write 256-bit vector loops and avoid SSE/AVX transition penalties.

```nasm
; void add8(float *dst, const float *a, const float *b)  n=8 floats
vmovups ymm0, [rsi]
vaddps  ymm0, ymm0, [rdx]       ; dst, src1, src2 (non-destructive)
vmovups [rdi], ymm0
vzeroupper
ret
```
- VEX instructions take three operands and leave sources intact; xmm forms (`vaddps xmm0, xmm1, xmm2`) zero the upper bits of ymm.
- AVX2 adds 256-bit integer ops (`vpaddd ymm`), gathers and variable shifts; FMA (`vfmadd231ps`) is a separate CPUID feature.
- `vmovaps` requires 32-byte alignment for ymm; `vmovups` does not. VEX-encoded memory operands of arithmetic ops need no alignment (except explicit aligned moves).
- Execute `vzeroupper` before returning to code that may use legacy SSE or before calls to unknown functions; this avoids mixed-state penalties on affected microarchitectures.
- Use requires CPUID AVX plus OSXSAVE and XGETBV(0) having bits 1 and 2 set (see cpuid-feature-detect).

## Gotchas
- Lane-crossing shuffles are limited: many AVX ops work on two independent 128-bit lanes.
- Calling convention: ymm registers are caller-saved on SysV; on Win64 xmm6-xmm15 low 128 bits are callee-saved and the upper halves are not.

## Self-check
Vectorise a float array sum with ymm, handle the tail with scalar code, and compare to the C result.
