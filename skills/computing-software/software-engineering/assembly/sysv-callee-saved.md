---
id: computing-software.software-engineering.assembly.sysv-callee-saved
name: sysv-callee-saved
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, sysv-callee-saved, asm-abi-sysv]
level: practitioner
status: docs-checked
description: "System V AMD64 register preservation: callee-saved RBX RBP R12-R15, scratch registers, direction flag, and control-word rules."
sources:
  - https://raw.githubusercontent.com/hjl-tools/x86-psABI/master/low-level-sys-info.tex
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SysV callee-saved and scratch registers
**Goal:** know which registers a function must preserve.

- Callee-saved (must be restored before return): `rbx`, `rbp`, `r12`, `r13`, `r14`, `r15`, and `rsp`.
- Caller-saved (scratch): `rax`, `rcx`, `rdx`, `rsi`, `rdi`, `r8`-`r11`, and `xmm0`-`xmm15`; the mmx, x87 (`st0`-`st7`) and mask registers are temporaries too.
- `r10` carries a function's static chain pointer; `r11` is a scratch register that is not used for arguments, so PLT code can use it without spilling.
- Other user flags are not preserved, but the direction flag must be clear on entry and return. MXCSR control bits and the x87 control word are callee-saved; MXCSR status bits and the x87 status word are caller-saved.
```nasm
; uses rbx and r12 as long-lived values
func:
    push rbx
    push r12
    sub  rsp, 8              ; entry 8 mod 16, two pushes leave 8 mod 16, so pad 8
    ...
    add  rsp, 8
    pop  r12
    pop  rbx
    ret
```
(At entry `rsp + 8` is a multiple of 16, so `rsp` is 8 mod 16; two pushes keep it 8 mod 16, so the extra 8 restores 16-byte alignment before any call.)

## Gotchas
- Values you need after a `call` must live in callee-saved registers or on the stack.
- Clobbering `rbx` in a function called from C breaks the caller in ways that appear far from the cause.

## Self-check
Write a function that calls `strlen` twice and keeps both arguments across the calls using rbx and r12.

## Checked
2026-11-08. Confirmed against the x86-64 psABI source: register usage table (rbx, rbp, rsp, r12-r15 preserved; r10 static chain; r11 temporary and PLT scratch), direction flag rule, MXCSR / x87 control-word / status-word rules, and the `(%rsp + 8)` entry alignment. Removed: "no vector register is preserved" as worded (replaced by the table's xmm0-xmm15 temporaries) and the specific MXCSR "bits 6-15" range (not stated on the cited source). Not run.
Method: documentation only; no commands were run.
