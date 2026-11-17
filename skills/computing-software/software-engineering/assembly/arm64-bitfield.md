---
id: computing-software.software-engineering.assembly.arm64-bitfield
name: arm64-bitfield
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, arm64-bitfield, asm-arm64-integer]
level: advanced
status: draft
description: "AArch64 bitfield instructions UBFX, SBFX, BFI, BFXIL, UBFIZ and the aliases LSL/LSR/ASR/SXT/UXT that are implemented as UBFM and SBFM."
sources:
  - https://developer.arm.com/documentation/ddi0487/latest
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Bitfield operations
**Goal:** extract, insert and extend fields in one instruction.

```asm
ubfx x0, x1, #8, #4        // x0 = (x1 >> 8) & 0xF
sbfx x0, x1, #8, #4        // same, sign-extended
bfi  x0, x1, #16, #8       // insert low 8 bits of x1 at bit 16 of x0
bfxil x0, x1, #4, #8       // insert x1[11:4] into low bits of x0
ubfiz x0, x1, #3, #5       // zero x0, insert 5 bits at bit 3
sxtw x0, w1                // sign-extend word
uxtb w0, w1                // zero-extend byte
lsl  x0, x1, #3            // alias of ubfm
```
- `lsl`/`lsr`/`asr` with an immediate, `sxtb/sxth/sxtw`, `uxtb/uxth` and the extract/insert names are assembler aliases of `ubfm`, `sbfm` and `bfm`; disassemblers print the most specific alias.
- `extr x0, x1, x2, #n` extracts a field spanning two registers (funnel shift); `ror` with an immediate is an alias of it.
- `bfi` preserves the other bits of the destination, so it reads the old value.

## Gotchas
- Operand order is lsb then width for the friendly names, but raw `ubfm` takes immr/imms; use the friendly aliases.
- Field must fit in the register width (`lsb + width <= 64`).

## Self-check
Pack three fields into a 32-bit word with `bfi` and unpack them with `ubfx`.
