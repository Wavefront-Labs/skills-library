---
id: computing-software.software-engineering.assembly.avx512-masking
name: avx512-masking
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, avx512-masking, asm-x86-simd]
level: sme
status: draft
description: "AVX-512 on x86-64: ZMM registers, K mask registers, merge and zeroing masking, embedded broadcast, tail handling and feature subsets."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# AVX-512 masking and ZMM
**Goal:** use per-lane masks to handle tails and conditionals without scalar fixups.

- 32 vector registers zmm0-zmm31 (xmm/ymm aliases) and eight mask registers k0-k7; EVEX encoding.
- Mask syntax: `{k1}` merges (unselected lanes keep the old destination), `{k1}{z}` zeroes them. `k0` cannot be used as a writemask.
```nasm
; sum floats with a masked tail; rcx = remaining count (< 16)
mov     eax, -1
bzhi    eax, eax, ecx            ; low rcx bits set (BMI2)
kmovw   k1, eax
vmovups zmm0{k1}{z}, [rsi]       ; masked load; masked-off lanes do not fault
vaddps  zmm1{k1}, zmm1, zmm0
vaddps  zmm2, zmm3, dword [rdi]{1to16}   ; embedded broadcast of a scalar
```
- Subsets are separate CPUID bits: AVX512F (base), BW (byte/word), DQ, VL (128/256-bit forms), CD, and others; require the one you use.
- OS support needs XCR0 bits 5, 6, 7 (opmask, upper ZMM, ZMM16-31) in addition to bits 1, 2.
- Heavy 512-bit use lowered clock speeds on some earlier Intel server parts; measure on the target (unconfirmed for newer cores).

## Gotchas
- Not available on all CPUs, including some recent consumer parts; always dispatch at run time.
- Compare instructions write mask registers (`vcmpps k1, zmm0, zmm1, 1`), not vector registers.

## Self-check
Implement `clamp_negative_to_zero` for n not a multiple of 16 using only masked ops.
