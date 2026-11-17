---
id: computing-software.software-engineering.assembly.nzcv-flags
name: nzcv-flags
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, nzcv-flags, asm-arm64-registers]
level: practitioner
status: draft
description: "AArch64 NZCV condition flags: which instructions set them, the carry-means-no-borrow rule on subtraction, and signed/unsigned condition codes."
sources:
  - https://developer.arm.com/documentation/ddi0487/latest
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# NZCV condition flags
**Goal:** pick the right condition code and set flags only when intended.

- Flags are N (negative), Z (zero), C (carry), V (overflow). Only instructions with an `s` suffix (`adds`, `subs`, `ands`, `bics`) and the aliases `cmp`, `cmn`, `tst` set them; plain `add`/`sub` do not.
- After a subtraction C=1 means no borrow, which means the first operand was unsigned greater than or equal to the second.
- Condition codes: `eq ne` (Z); `hs`(=cs) `lo`(=cc) unsigned >=, <; `hi` unsigned >; `ls` unsigned <=; `ge lt gt le` signed; `mi pl` sign; `vs vc` overflow; `al` always.
```asm
cmp  x0, x1
b.hi bigger_unsigned     // x0 > x1 unsigned
b.gt bigger_signed       // x0 > x1 signed
// 128-bit add: (x1:x0) + (x3:x2)
adds x0, x0, x2
adc  x1, x1, x3          // adc consumes C
```
- `adc`/`sbc` use the carry; start a chain with `adds`/`subs`.

## Gotchas
- Mixing up `hs`/`lo` with `hi`/`ls` is the usual off-by-one bug.
- Flags are not preserved across calls (AAPCS64 does not preserve NZCV).

## Self-check
Compare 0x80000000 and 1 as w registers; predict which of `hi` and `gt` is taken.
