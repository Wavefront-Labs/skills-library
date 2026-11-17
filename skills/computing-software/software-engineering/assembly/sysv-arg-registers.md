---
id: computing-software.software-engineering.assembly.sysv-arg-registers
name: sysv-arg-registers
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, sysv-arg-registers, asm-abi-sysv]
level: practitioner
status: docs-checked
description: "System V AMD64 argument and return registers: RDI RSI RDX RCX R8 R9, XMM0-7, stack arguments, return in RAX/RDX/XMM0, and AL for variadic calls."
sources:
  - https://raw.githubusercontent.com/hjl-tools/x86-psABI/master/low-level-sys-info.tex
  - https://man7.org/linux/man-pages/man2/syscall.2.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SysV AMD64 argument registers
**Goal:** call and implement functions on Linux/BSD/macOS x86-64 correctly.

- Integer/pointer arguments in order: `rdi, rsi, rdx, rcx, r8, r9`. Floating arguments: `xmm0`-`xmm7`. Memory-class arguments go on the stack, pushed right to left; the stack frame table puts the return address at `8(%rbp)` after the frame is set up, so at entry the first stack argument is at `[rsp+8]`.
- Return: INTEGER-class values in `rax` then `rdx`, SSE-class in `xmm0` then `xmm1`, `long double` (X87) in `st0`, `_Complex long double` real part in `st0` and imaginary in `st1`. A MEMORY-class return gets its address in `rdi` and returns that address in `rax`.
- Variadic callee: the caller sets `al` to an upper bound on the number of vector registers used (0 to 8 inclusive).
```nasm
extern printf
section .rodata
fmt: db "%d %f", 10, 0
dbl: dq 2.5
section .text
global main
main:
    sub  rsp, 8                    ; align (entry rsp = 8 mod 16)
    lea  rdi, [rel fmt]
    mov  esi, 42
    movsd xmm0, [rel dbl]
    mov  eax, 1                    ; one vector register used
    call printf wrt ..plt
    xor  eax, eax
    add  rsp, 8
    ret
```
- The Linux kernel syscall convention is different: the 4th argument is in `r10`, not `rcx` (syscall(2): x86-64 arg registers rdi, rsi, rdx, r10, r8, r9).

## Gotchas
- A missing `al` setup before calling a variadic function means the callee gets no valid bound on vector registers used; set it every time, even to 0.
- `r10` is also the static chain pointer, and `r11` is never an argument register.

## Self-check
Write `long sum6(long,long,long,long,long,long)` in assembly and call it from C.

## Checked
2026-11-08. Confirmed against the x86-64 psABI source (argument register sequences, memory args right to left, return-value register rules, MEMORY return in rdi/rax, `al` upper bound 0-8 for variadic calls, `r10` static chain, `r11` scratch) and the Linux syscall(2) page (x86-64 syscall argument registers). Removed: "`printf` uses it to decide whether to save xmm registers" and "arguments extended to 32 bits in practice" (not on the cited pages), and the 128-bit-in-rdx wording (replaced by the INTEGER-class rule). The `al` handling in the example is as the ABI states; the example was not assembled.
Method: documentation only; no commands were run.
