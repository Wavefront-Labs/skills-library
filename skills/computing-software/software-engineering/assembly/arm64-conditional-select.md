---
id: computing-software.software-engineering.assembly.arm64-conditional-select
name: arm64-conditional-select
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, arm64-conditional-select, asm-arm64-control]
level: practitioner
status: draft
description: "Branchless AArch64 code with CMP, CSEL, CSET, CSINC, CNEG and CCMP chains, including min/max/abs examples."
sources:
  - https://developer.arm.com/documentation/ddi0487/latest
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# CMP, CSEL, CSET, CCMP
**Goal:** remove short branches with conditional select.

```asm
// int max(int a, int b)
cmp   w0, w1
csel  w0, w0, w1, gt          // w0 = (w0 > w1) ? w0 : w1
ret
// abs
cmp   w0, #0
cneg  w0, w0, lt              // negate if less than zero
// boolean
cmp   x0, x1
cset  w0, eq                  // w0 = (x0 == x1)
// (a == 1 && b == 2)
cmp   x0, #1
ccmp  x1, #2, #0, eq          // if eq: compare x1 with 2, else NZCV = 0
b.eq  both
```
- `csel d, n, m, cond` picks n if the condition holds else m. `csinc`, `csinv`, `csneg` apply +1, invert, negate to the else operand; `cset`, `cinc`, `cneg` are aliases.
- `ccmp` makes a chain of compares: if the previous condition holds it compares, otherwise it loads the literal flags `#nzcv`.
- The condition code in `cset` is the one you want true; the assembler encodes the inverse into `csinc` internally.

## Gotchas
- Choose the `ccmp` fallback NZCV so the final condition fails when the first test failed.
- Branchless is not always faster: a well-predicted branch can beat a dependency chain.

## Self-check
Implement clamp(x, lo, hi) with two `csel` and compare to a branchy version.
