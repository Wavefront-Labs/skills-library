---
id: computing-software.software-engineering.assembly.sse-scalar-float
name: sse-scalar-float
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, sse-scalar-float, asm-x86-simd]
level: practitioner
status: draft
description: "Scalar float and double arithmetic with SSE/SSE2 on x86-64: moves, arithmetic, conversions, compares with UCOMISD and NaN handling."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
  - https://gitlab.com/x86-psABIs/x86-64-ABI
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# SSE/SSE2 scalar floating point
**Goal:** write double/float code with xmm registers (the x86-64 baseline, no x87 needed).

```nasm
; double hypot2(double a, double b)  a=xmm0, b=xmm1, result in xmm0
hypot2:
    mulsd xmm0, xmm0
    mulsd xmm1, xmm1
    addsd xmm0, xmm1
    ret
; constants
section .rodata
half: dq 0.5
section .text
    movsd xmm2, [rel half]
    cvtsi2sd xmm3, rdi          ; int64 -> double
    cvttsd2si rax, xmm0         ; truncate toward zero
    pxor xmm4, xmm4             ; zero (xorps works too)
```
- `ss` suffix is single (float), `sd` is double. Arithmetic: add, sub, mul, div, sqrt, min, max.
- `ucomisd a, b` sets ZF, PF, CF: unordered (NaN) sets all three. Test NaN with `jp`.
- `cvttsd2si` truncates; `cvtsd2si` rounds per MXCSR (default nearest-even).
- `movss`/`movsd` from memory zero the upper lanes; register-to-register forms merge and keep the upper bits (a false dependency; use `movaps` for full copies).

## Gotchas
- `cvtsi2sd` merges into the destination; clear it first (`pxor`) to avoid a dependency chain.
- `minsd`/`maxsd` return the second operand if either is NaN, so argument order matters.

## Self-check
Compute `sqrt(x*x+y*y)` and test with NaN and infinity inputs.
