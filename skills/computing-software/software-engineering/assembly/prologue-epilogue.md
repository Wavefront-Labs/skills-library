---
id: computing-software.software-engineering.assembly.prologue-epilogue
name: prologue-epilogue
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, prologue-epilogue, asm-stack-frames]
level: practitioner
status: draft
description: "Function prologue and epilogue patterns on x86-64 and AArch64: frame pointer setup, local allocation, alignment, LEAVE and LDP/RET."
sources:
  - https://gitlab.com/x86-psABIs/x86-64-ABI
  - https://github.com/ARM-software/abi-aa
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Prologue and epilogue patterns
**Goal:** write a correct frame for functions with locals and calls.

```nasm
; x86-64 with frame pointer, 32 bytes of locals
func:
    push rbp
    mov  rbp, rsp
    sub  rsp, 32            ; entry 8 mod 16, push -> 0 mod 16, 32 keeps it
    mov  [rbp-8], rdi       ; locals via rbp
    ...
    leave                   ; mov rsp, rbp ; pop rbp
    ret
```
```asm
// AArch64
func:
    stp  x29, x30, [sp, #-48]!    // frame record + 32 bytes locals
    mov  x29, sp
    str  x0, [sp, #16]
    ...
    ldp  x29, x30, [sp], #48
    ret
```
- Keep `rsp` 16-byte aligned at calls (SysV, Win64) and `sp` always 16-byte aligned (AArch64).
- Frameless functions skip the frame pointer and address locals relative to `rsp`; compilers do this at -O2 unless `-fno-omit-frame-pointer`.
- Callee-saved registers are saved after the frame setup and restored in reverse order.
- The epilogue must undo exactly what the prologue did; `leave` is shorthand for the first two undo steps on x86.

## Gotchas
- Returning with `sp` off by 8 on x86-64 is the most common "return to garbage" bug.
- Any change to `sp` must be matched in CFI directives for unwinding (see gas-cfi-directives).

## Self-check
Write a function with locals, call `printf` inside, and confirm the alignment at the call in a debugger.
