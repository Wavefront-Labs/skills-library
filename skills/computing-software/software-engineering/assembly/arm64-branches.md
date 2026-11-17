---
id: computing-software.software-engineering.assembly.arm64-branches
name: arm64-branches
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, arm64-branches, asm-arm64-control]
level: practitioner
status: draft
description: "AArch64 branch instructions B, BL, BR, BLR, RET, B.cond: link register use, ranges, tail calls and why non-leaf functions must save LR."
sources:
  - https://developer.arm.com/documentation/ddi0487/latest
  - https://github.com/ARM-software/abi-aa
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# B, BL, BR, BLR, RET
**Goal:** call, return and jump correctly.

```asm
bl   callee               // x30 = return address; jump
blr  x16                  // indirect call
br   x17                  // indirect jump (no link)
b    other_function       // tail call: no link, callee returns to our caller
ret                       // jump to x30 (ret x1 uses x1)
b.eq label                // conditional
```
- Range: `b`/`bl` +-128 MiB; `b.cond`, `cbz`/`cbnz` +-1 MiB; `tbz`/`tbnz` +-32 KiB. The linker inserts veneers for out-of-range `b`/`bl` on common toolchains.
- `bl` overwrites `x30`, so a function that calls others must save and restore it (`stp x29, x30, [sp, #-16]!`), then `ret`.
- A leaf function can `ret` immediately without touching the stack.
- Branch-target identification may require `bti c` at indirect call targets (see pointer-auth-bti).

## Gotchas
- Forgetting to restore `x30` after a nested call makes `ret` loop to the wrong address.
- `br x30` works but `ret` is preferred: it gives the return predictor a hint.

## Self-check
Write `outer` calling `inner`, with a correct frame, and single-step to watch x30 change.
