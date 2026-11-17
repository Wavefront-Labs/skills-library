---
id: computing-software.software-engineering.assembly.x87-fpu-stack
name: x87-fpu-stack
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, x87-fpu-stack, asm-x87]
level: advanced
status: draft
description: "x87 FPU basics on x86-64: the eight-entry register stack, load/store forms, 80-bit long double, ABI rules and when you still meet x87."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
  - https://gitlab.com/x86-psABIs/x86-64-ABI
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# x87 stack registers and FLD/FSTP
**Goal:** read and write x87 code, mainly for `long double` and legacy routines.

- Eight 80-bit registers st0-st7 organised as a stack; operations push and pop.
```nasm
; long double add_ld(long double a, long double b)  SysV: both passed in memory
add_ld:
    fld  tword [rsp + 8]     ; push a
    fld  tword [rsp + 24]    ; push b
    faddp st1, st0           ; st1 = st1 + st0, pop
    ret                      ; result in st0
```
- Loads: `fld dword/qword/tword`, `fild` (integer); stores: `fst`, `fstp` (pop), `fistp`. Math: `fadd`, `fsub`, `fmul`, `fdiv`, `fsqrt`, `fxch`.
- `fucomip st0, st1` compares and sets ZF/PF/CF directly (then `fstp st0` to drop the extra value).
- SysV x86-64: `long double` is the 80-bit type, arguments of that class go on the stack and the result returns in st0; the x87 stack must be empty at function entry and exit.
- Win64 (MSVC) treats `long double` as a 64-bit double, so x87 is rare there.

## Gotchas
- Stack overflow beyond eight entries produces NaN; always balance pushes and pops.
- Mixing x87 and MMX state needs `emms`.

## Self-check
Write `fsqrt` of a long double argument and check with `printf("%Lf")` in a C driver.
