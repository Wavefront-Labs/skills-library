---
id: computing-software.software-engineering.assembly.movz-movk-immediates
name: movz-movk-immediates
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, movz-movk-immediates, asm-arm64-integer]
level: practitioner
status: draft
description: "Build 16/32/48/64-bit constants on AArch64 with MOVZ, MOVK and MOVN, how the assembler's MOV picks an encoding, and literal pool alternatives."
sources:
  - https://developer.arm.com/documentation/ddi0487/latest
  - https://sourceware.org/binutils/docs/as/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# MOVZ / MOVK / MOVN constant building
**Goal:** load any constant efficiently.

```asm
movz x0, #0x1234               // x0 = 0x1234, other bits zero
movz x0, #0x1234, lsl #16      // 0x12340000
movk x0, #0xabcd, lsl #32      // replace only bits 47:32
movn x0, #0                    // x0 = ~0 = -1
mov  x0, #0x123456789abc       // assembler expands to movz + movk + movk
mov  w1, #0xff00ff00           // may become a single orr (logical immediate)
```
- Each 16-bit chunk costs one instruction: a 64-bit constant needs up to four.
- `mov xN, #imm` is an assembler alias; it chooses `movz`, `movn` or `orr` with a logical immediate, whichever encodes the value.
- Negative small values use `movn` (inverted immediate).
- Alternatives: PC-relative literal load (`ldr x0, literal_label`), or `adrp/add` for addresses. Compilers load floating constants with `ldr d0, =...` or `fmov d0, #imm` (only a small set of FP immediates is encodable).

## Gotchas
- `movk` without a prior `movz`/`mov` merges into stale bits.
- Shift amount for `movz/movk` is a multiple of 16 (0, 16, 32, 48; only 0, 16 for `w`).

## Self-check
Load 0xDEADBEEFCAFEBABE and read it back in a debugger.
