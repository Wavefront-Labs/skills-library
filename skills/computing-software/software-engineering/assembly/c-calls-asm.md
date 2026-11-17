---
id: computing-software.software-engineering.assembly.c-calls-asm
name: c-calls-asm
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, c-calls-asm, asm-interop]
level: practitioner
status: draft
description: "Call an assembly function from C: prototype, export symbol, ABI-correct register use for x86-64 SysV and AArch64, and build commands."
sources:
  - https://gitlab.com/x86-psABIs/x86-64-ABI
  - https://github.com/ARM-software/abi-aa
  - https://www.nasm.us/doc/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Calling assembly from C
**Goal:** link a hand-written routine into a C program.

```c
/* main.c */
#include <stdio.h>
extern long add2(long a, long b);
int main(void) { printf("%ld\n", add2(40, 2)); return 0; }
```
```nasm
; add2.asm (x86-64 SysV)
global add2
section .text
add2:
    lea  rax, [rdi + rsi]
    ret
```
```asm
// add2.s (AArch64)
    .globl add2
    .type  add2, %function
add2:
    add  x0, x0, x1
    ret
    .size add2, .-add2
```
```sh
nasm -f elf64 add2.asm -o add2.o && gcc main.c add2.o -o demo && ./demo
```
- Arguments arrive in the ABI's registers (`rdi, rsi`; `x0, x1`); return in `rax`/`x0`.
- Preserve callee-saved registers and stack alignment if the routine calls other code or uses them.
- A prototype with the right types matters: `int` arguments are 32-bit and leave the upper half of the register undefined.
- For GAS sources add `.section .note.GNU-stack,"",@progbits` at the end to avoid an executable-stack marking.

## Gotchas
- Declaring the function `int` when it returns `long` truncates the result at the call site.
- Windows needs the Win64 convention (`rcx, rdx`), so the same file does not work there.

## Self-check
Add a third argument and verify the register it arrives in with a debugger.
