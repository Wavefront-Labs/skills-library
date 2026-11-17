---
id: computing-software.software-engineering.assembly.arm64-arith-logic
name: arm64-arith-logic
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, arm64-arith-logic, asm-arm64-integer]
level: practitioner
status: draft
description: "AArch64 add, subtract and logical instructions with shifted or extended register operands and immediates, plus common aliases."
sources:
  - https://developer.arm.com/documentation/ddi0487/latest
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Arithmetic and logic with shifted operands
**Goal:** fold shifts and extensions into data-processing instructions.

```asm
add  x0, x1, x2                 // register
add  x0, x1, x2, lsl #3         // x1 + (x2 << 3): array index scaling
add  x0, x1, w2, uxtw #2        // zero-extend w2 then shift
add  x0, x1, #4095              // 12-bit immediate
add  x0, x1, #1, lsl #12        // immediate shifted left 12
subs x0, x1, #1                 // sets flags
and  x0, x1, #0xff              // logical immediate (encodable patterns only)
orr  x0, x1, x2, ror #8
eor  w0, w1, w2 ; bic x0, x1, x2 ; orn x0, x1, x2
mvn  x0, x1                     // alias: orn x0, xzr, x1
tst  x0, #1                     // alias: ands xzr, x0, #1
```
- Add/sub immediates are 12 bits, optionally shifted left by 12. Larger constants need `movz/movk` first.
- Logical immediates must be a repeating, rotated run of ones (for example 0xFF, 0x0F0F0F0F0F0F0F0F); arbitrary values are not encodable and the assembler reports an error.
- Shifted register operands allow `lsl lsr asr` (and `ror` for logical ops).

## Gotchas
- `add` with `sp` as destination or source uses the extended-register or immediate forms, not the shifted-register one.
- Writing `w` registers zeroes the upper halves.

## Self-check
Encode `x << 3 + y` and `0x12345` into one valid instruction each, or explain why not.
