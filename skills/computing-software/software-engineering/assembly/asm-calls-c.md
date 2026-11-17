---
id: computing-software.software-engineering.assembly.asm-calls-c
name: asm-calls-c
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, asm-calls-c, asm-interop]
level: practitioner
status: draft
description: "Call C library functions from assembly: stack alignment, PLT calls, varargs setup, preserving values across calls, with x86-64 and AArch64 puts examples."
sources:
  - https://gitlab.com/x86-psABIs/x86-64-ABI
  - https://github.com/ARM-software/abi-aa
  - https://www.nasm.us/doc/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Calling C from assembly
**Goal:** use libc from an assembly `main`.

```nasm
; hi.asm  (nasm -f elf64 hi.asm && gcc hi.o -o hi)
default rel
extern puts
global main
section .rodata
msg: db "hello", 0
section .text
main:
    sub  rsp, 8                    ; entry rsp = 8 mod 16 -> align to 16
    lea  rdi, [msg]
    call puts wrt ..plt
    xor  eax, eax                  ; return 0
    add  rsp, 8
    ret
```
```asm
// hi.s (AArch64, ELF)
    .globl main
main:
    stp  x29, x30, [sp, #-16]!
    mov  x29, sp
    adrp x0, msg
    add  x0, x0, :lo12:msg
    bl   puts
    mov  w0, #0
    ldp  x29, x30, [sp], #16
    ret
    .section .rodata
msg: .asciz "hello"
```
- Let the `gcc` driver link so the C runtime startup code calls your `main`.
- Variadic functions on x86-64 (`printf`) need `al` set to the number of vector registers used (0 if none).
- Values you need after the call must be in callee-saved registers or on the stack.
- On Win64 reserve 32 bytes of shadow space and use `rcx, rdx, r8, r9`.

## Gotchas
- Misaligned stack at the call crashes inside libc on `movaps`.
- AArch64 must save `x30` before `bl`, or `ret` returns to itself.

## Self-check
Call `printf("%d\n", 7)` from assembly and print correct output.
