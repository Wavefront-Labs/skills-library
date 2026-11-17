---
id: computing-software.software-engineering.assembly.freestanding-start
name: freestanding-start
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, freestanding-start, asm-baremetal]
level: advanced
status: draft
description: "Write a freestanding program with a custom _start: Linux process entry stack layout, argc/argv access, alignment, no-libc build flags and exit."
sources:
  - https://gitlab.com/x86-psABIs/x86-64-ABI
  - https://man7.org/linux/man-pages/man2/syscall.2.html
  - https://sourceware.org/binutils/docs/ld/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Freestanding _start and custom entry
**Goal:** start a program without the C runtime.

- At process entry on Linux x86-64: `rsp` points to `argc`, followed by `argv[0..argc-1]`, a NULL, the `envp` pointers, a NULL, then the auxiliary vector. `rsp` is 16-byte aligned. The ABI says `rbp` should be zeroed to mark the outermost frame, and `rdx` holds a function pointer for `atexit` registration (zero from the kernel).
```nasm
global _start
extern cmain                       ; int cmain(int argc, char **argv)
section .text
_start:
    xor  ebp, ebp
    mov  rdi, [rsp]                ; argc
    lea  rsi, [rsp + 8]            ; argv
    and  rsp, -16                  ; keep alignment (already aligned at entry)
    call cmain                     ; callee sees rsp = 8 mod 16
    mov  edi, eax
    mov  eax, 231                  ; exit_group
    syscall
```
```asm
// AArch64: sp points to argc at entry, 16-byte aligned
_start:
    mov  x29, xzr
    ldr  x0, [sp]                  // argc
    add  x1, sp, #8                // argv
    bl   cmain
    mov  x8, #94                   // exit_group
    svc  #0
```
```sh
gcc -nostdlib -static -ffreestanding -fno-stack-protector -o prog start.o main.c
```
- With `-nostdlib` there is no `printf`, no `memcpy`, no TLS setup; compilers may still emit calls to `memcpy`/`memset`, so provide them.
- Thread-local storage, stack protector and `errno` need runtime support you must write or avoid.

## Gotchas
- Forgetting to exit makes the CPU run off the end of `_start` and crash.
- The kernel sets up the stack but not the red zone or signal stack; handle those yourself if needed.

## Self-check
Print each command-line argument with raw `write` calls and exit with `argc`.
