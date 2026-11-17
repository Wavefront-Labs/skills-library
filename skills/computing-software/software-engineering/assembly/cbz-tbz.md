---
id: computing-software.software-engineering.assembly.cbz-tbz
name: cbz-tbz
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, cbz-tbz, asm-arm64-control]
level: practitioner
status: draft
description: "AArch64 compare-and-branch and test-bit-and-branch: CBZ, CBNZ, TBZ, TBNZ with ranges, no flag effect, and typical loop uses."
sources:
  - https://developer.arm.com/documentation/ddi0487/latest
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# CBZ, CBNZ, TBZ, TBNZ
**Goal:** branch on zero or a single bit without a separate compare.

```asm
// strlen-like loop
    mov  x1, x0
1:  ldrb w2, [x1], #1
    cbnz w2, 1b              // loop while byte != 0
    sub  x0, x1, x0
    sub  x0, x0, #1
    ret

    tbz  x0, #63, positive   // branch if bit 63 clear (non-negative)
    tbnz w1, #0, odd         // bit 0 set
```
- `cbz`/`cbnz` test a register against zero; `tbz`/`tbnz` test one bit by number (0-63, use a `w` register name for bits below 32).
- None of them touches the flags; they cannot test arbitrary conditions.
- Ranges: `cbz`/`cbnz` +-1 MiB, `tbz`/`tbnz` +-32 KiB. For far targets invert the condition and branch over an unconditional `b`.
- Local numeric labels (`1:` with `1b`/`1f`) are a GNU as feature for tight loops.

## Gotchas
- The assembler errors on out-of-range `tbz` targets; the linker does not fix them with veneers on all toolchains (unconfirmed), so restructure.
- Bit number is a literal, not a register.

## Self-check
Test the sign of a 64-bit value with `tbz` and compare its size with `cmp`+`b.pl`.
