---
id: computing-software.software-engineering.assembly.shifts-rotates-bitops
name: shifts-rotates-bitops
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, shifts-rotates-bitops, asm-x86-integer]
level: practitioner
status: draft
description: "x86-64 shifts, rotates and bitwise ops: count masking, flag effects, arithmetic vs logical right shift, and the common bit-test idioms."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Shifts, rotates and bitwise ops
**Goal:** manipulate bits with correct flag and count semantics.

```nasm
shl  eax, 3            ; multiply by 8 (logical left)
shr  eax, 1            ; unsigned divide by 2
sar  eax, 1            ; signed divide by 2 (rounds toward negative infinity)
rol  eax, 8 ; ror eax, 8
shl  rax, cl           ; count in CL only
and  eax, 0xFF ; or eax, 1 ; xor eax, eax ; not eax
bt   rax, 5            ; CF = bit 5
bts  rax, 5            ; set bit, old value in CF
shld rdx, rax, 4       ; double-precision shift
```
- The count is masked to 5 bits (32-bit ops) or 6 bits (64-bit ops).
- A count of 0 leaves flags unchanged; `and`/`or`/`xor`/`test` clear CF and OF; `not` changes no flags.
- `sar` for signed division by 2^n rounds toward negative infinity, unlike C `/`, so compilers add a bias for negative inputs.
- `xor reg, reg` is the standard zeroing idiom and breaks dependencies.

## Gotchas
- Shift count from a variable must be in `cl`, unless BMI2 `shlx/shrx/sarx` is available (any register count, no flags).
- Rotating through carry (`rcl`/`rcr`) is slow on many cores; avoid in hot loops.

## Self-check
Implement `extract_bits(x, lo, len)` using shr and and, then compare with `bextr` if BMI1 exists.
