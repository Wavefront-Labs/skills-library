---
id: computing-software.software-engineering.assembly.division-by-constant
name: division-by-constant
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, division-by-constant, asm-x86-bitmanip]
level: sme
status: draft
description: "Replace division by a compile-time constant with a multiply-high and shift, shown for unsigned divide-by-10, plus signed and power-of-two cases."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Division by constants via multiply
**Goal:** understand and reproduce what compilers do for `x / C`.

- Unsigned 32-bit `x / 10` equals `(x * 0xCCCCCCCD) >> 35` computed in 64 bits:
```nasm
; edi = x (uint32), returns eax = x / 10
mov  eax, edi              ; zero-extends into rax
mov  ecx, 0xCCCCCCCD       ; 3435973837
imul rax, rcx              ; 64-bit product
shr  rax, 35
ret
```
- The magic multiplier is about 2^k / C rounded up; the shift removes k. Correctness depends on the pair (multiplier, shift) being proven for the full input range (Hacker's Delight / Granlund-Montgomery method).
- Signed division needs a fix-up: add the sign bit of the result (or a bias for negative dividends) so the quotient truncates toward zero like C.
- Division by 2^n: unsigned is `shr`; signed is `lea/add bias` then `sar`, e.g. for n=2: `lea eax,[rdi+3]; test edi,edi; cmovns eax,edi; sar eax,2`.
- Remainder: `x - q*C`, using `imul` and `sub`.

## Gotchas
- Do not hand-pick magic numbers; generate with a compiler (compile `x/C` at -O2) or a verified tool such as libdivide.
- Valid only for fixed C; variable divisors must use `div`.

## Self-check
Exhaustively compare the sequence against `div` for all 2^32 inputs in a test harness.
