---
id: computing-software.software-engineering.assembly.neon-vector-registers
name: neon-vector-registers
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, neon-vector-registers, asm-arm64-simd]
level: practitioner
status: draft
description: "AArch64 NEON basics: V registers, arrangement specifiers like 4S and 16B, lane operations, reductions and callee-saved low halves."
sources:
  - https://developer.arm.com/documentation/ddi0487/latest
  - https://github.com/ARM-software/abi-aa
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# NEON vector registers and arrangements
**Goal:** write 128-bit SIMD code in A64 syntax.

- `v0`-`v31` are 128 bits; operations name an arrangement: `.16b`, `.8h`, `.4s`, `.2d` (full) and `.8b`, `.4h`, `.2s`, `.1d` (low 64 bits). Scalar views: `b h s d q`.
```asm
ld1   {v0.4s}, [x0]               // load four 32-bit lanes
ld1   {v1.4s}, [x1]
add   v2.4s, v0.4s, v1.4s         // integer lane add
fmla  v3.4s, v0.4s, v1.4s         // v3 += v0 * v1
st1   {v2.4s}, [x2]
dup   v4.4s, w3                   // broadcast
movi  v5.4s, #0
addv  s6, v0.4s                   // horizontal add
umov  w4, v0.s[1]                 // lane to GPR
cnt   v7.16b, v0.16b              // popcount per byte
```
- Writing a scalar view (`d0`, `s0`) zeroes the rest of the register.
- AAPCS64: `v0`-`v7` carry arguments and results; the low 64 bits (`d8`-`d15`) of `v8`-`v15` are callee-saved, upper halves are not.
- Advanced SIMD is mandatory in AArch64 application profile cores, no feature test needed on Linux.

## Gotchas
- Mixing arrangements across operands is an assembler error; `.4s` pairs with `.4s`.
- Reductions across lanes are slower than lane-wise ops; reduce once at the end.

## Self-check
Sum a float array with `fadd v.4s` in the loop and `faddp` reductions after it; compare to scalar C.
