---
id: computing-software.software-engineering.assembly.cpuid-feature-detect
name: cpuid-feature-detect
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, cpuid-feature-detect, asm-x86-simd]
level: advanced
status: draft
description: "Detect x86 CPU features with CPUID and XGETBV, correct bit positions for SSE4.2, AVX, AVX2, BMI and AVX-512, and runtime dispatch."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# CPUID feature detection and dispatch
**Goal:** choose an instruction-set path at run time safely.

```nasm
; returns eax = 1 if AVX2 usable
has_avx2:
    push rbx                   ; cpuid clobbers rbx (callee-saved)
    mov  eax, 1
    cpuid
    mov  r8d, ecx
    and  r8d, (1<<27)|(1<<28)  ; OSXSAVE and AVX
    cmp  r8d, (1<<27)|(1<<28)
    jne  .no
    xor  ecx, ecx
    xgetbv                     ; XCR0 in edx:eax
    and  eax, 6                ; XMM and YMM state enabled by OS
    cmp  eax, 6
    jne  .no
    mov  eax, 7
    xor  ecx, ecx
    cpuid
    shr  ebx, 5
    and  ebx, 1                ; leaf 7 EBX bit 5 = AVX2
    mov  eax, ebx
    pop  rbx
    ret
.no:
    xor  eax, eax
    pop  rbx
    ret
```
- Leaf 1 ECX: SSE3 bit 0, SSSE3 9, FMA 12, CX16 13, SSE4.1 19, SSE4.2 20, MOVBE 22, POPCNT 23, XSAVE 26, OSXSAVE 27, AVX 28. EDX: SSE 25, SSE2 26.
- Leaf 7 subleaf 0 EBX: BMI1 bit 3, AVX2 5, BMI2 8, ERMS 9, AVX512F 16.
- Check the maximum leaf (cpuid with eax=0) before reading leaf 7.
- In C use `__builtin_cpu_supports("avx2")` or function multiversioning; check the SDM CPUID table for any other bit.

## Gotchas
- CPU support is not enough: the OS must save the wider state (XGETBV check).
- Cache the result once at startup in a function pointer rather than calling cpuid per call (cpuid is slow and may trap in VMs).

## Self-check
Print every bit above for your CPU and cross-check with `lscpu` flags.
