---
id: computing-software.software-engineering.assembly.ldp-stp-pairs
name: ldp-stp-pairs
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, ldp-stp-pairs, asm-arm64-loadstore]
level: practitioner
status: draft
description: "AArch64 LDP/STP load and store pairs: pre- and post-index forms for frame setup, offset ranges, and why they replace push and pop."
sources:
  - https://developer.arm.com/documentation/ddi0487/latest
  - https://github.com/ARM-software/abi-aa
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# LDP/STP pairs
**Goal:** save and restore register pairs and copy memory two registers at a time.

```asm
func:
    stp  x29, x30, [sp, #-16]!    // push frame pointer and LR
    mov  x29, sp
    ...
    ldp  x29, x30, [sp], #16      // pop
    ret
```
- `stp`/`ldp` move two registers (`x`, `w`, or SIMD `d`/`q`) to/from adjacent memory. Offset is a signed 7-bit value scaled by the register size (x: -512..504 in steps of 8).
- There is no push/pop; pre-index (`!`) and post-index forms emulate them while keeping `sp` 16-byte aligned.
- `ldnp`/`stnp` are non-temporal hints. `ldpsw` loads a pair of signed words into x registers.
```asm
ldp  q0, q1, [x1], #32     // copy 32 bytes
stp  q0, q1, [x0], #32
```

## Gotchas
- `ldp x0, x0, [..]` (same destination twice) is unpredictable.
- `sp` must stay 16-byte aligned whenever it is used as a base register for loads and stores, so save registers in pairs even if one is padding.

## Self-check
Write a prologue saving x19-x22 plus the frame pair and a matching epilogue; confirm the offsets stay inside the immediate range.
