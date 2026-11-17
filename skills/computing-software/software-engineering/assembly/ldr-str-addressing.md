---
id: computing-software.software-engineering.assembly.ldr-str-addressing
name: ldr-str-addressing
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, ldr-str-addressing, asm-arm64-loadstore]
level: practitioner
status: draft
description: "AArch64 load/store addressing modes: scaled unsigned offset, unscaled LDUR/STUR, pre/post-index writeback, register offset with extend, literal loads."
sources:
  - https://developer.arm.com/documentation/ddi0487/latest
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# LDR/STR addressing modes
**Goal:** choose the addressing form that encodes your access.

```asm
ldr  x0, [x1]                 // base
ldr  x0, [x1, #16]            // unsigned offset, multiple of 8 for x, 0..32760
ldur x0, [x1, #-8]            // unscaled signed offset -256..255
ldr  x0, [x1, #8]!            // pre-index: x1 += 8, then load
ldr  x0, [x1], #8             // post-index: load, then x1 += 8
ldr  w0, [x1, x2, lsl #2]     // register offset, scaled (int array)
ldr  x0, [x1, w2, sxtw #3]    // sign-extended 32-bit index
ldr  x0, label                // PC-relative literal, +-1 MiB
ldrb w0, [x1] ; ldrsb x0, [x1] ; ldrsw x0, [x1] ; strh w0, [x1]
```
- Sizes: `b` byte, `h` half, `w` word, `x` double; `ldrs*` sign-extends; plain loads zero-extend.
- The scaled unsigned 12-bit offset is multiplied by the access size; for out-of-range offsets use `ldur`, or add the offset into a register first.
- When `sp` is the base it must be 16-byte aligned at the access.

## Gotchas
- Pre/post-index with the same register as the loaded value is unpredictable.
- Writeback forms cannot be mixed with register-offset addressing.

## Self-check
Write a loop summing a `uint32_t` array with a post-index load and verify against C.
