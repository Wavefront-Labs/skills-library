---
id: computing-software.software-engineering.assembly.nasm-syntax-sections
name: nasm-syntax-sections
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, nasm-syntax-sections, asm-nasm]
level: intro
status: docs-checked
description: "NASM basics: Intel operand order, sections, labels and local labels, memory brackets versus addresses, and building a Linux x86-64 executable."
sources:
  - https://www.nasm.us/doc/nasm02.html
  - https://www.nasm.us/doc/nasm03.html
  - https://www.nasm.us/doc/nasm08.html
  - https://www.nasm.us/doc/nasm09.html
  - https://raw.githubusercontent.com/torvalds/linux/master/arch/x86/entry/syscalls/syscall_64.tbl
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# NASM syntax, sections and labels
**Goal:** write and build a standalone NASM program.

```nasm
bits 64
default rel
global _start
section .rodata
msg: db "Hello", 10
len: equ $ - msg
section .text
_start:
    mov  eax, 1              ; write (number 1)
    mov  edi, 1
    lea  rsi, [rel msg]
    mov  edx, len
    syscall
    mov  eax, 60             ; exit (number 60)
    xor  edi, edi
    syscall
```
Build and run: `nasm -f elf64 hello.asm -o hello.o && ld hello.o -o hello && ./hello`
- A source line is `label: instruction operands ; comment`; each field is optional. Register names carry no `%` prefix.
- A memory reference (effective address) is an expression in square brackets: `[wordvar]`, `[wordvar+1]`.
- In 64-bit mode NASM generates absolute addresses by default; the `REL` keyword makes it produce RIP-relative ones, and `default rel` makes that the default. `ABS` overrides `REL`.
- The elf32, elf64 and elfx32 formats produce ELF object files (default extension `.o`); `elf` is a synonym for `elf32`.
- Sections: `.text`, `.rodata`, `.data` and `.bss` are the Unix-style names; in `bin` output `.bss` defaults to nobits. `resb`/`resq` reserve space.
- A label beginning with a single `.` is local to the previous non-local label (so `.loop` can recur); NASM names it `label1.loop`, reachable from elsewhere. Symbols beginning with `..` are special.
- `$` is the assembly position at the start of the line containing the expression, `$$` the start of the current section; `len: equ $ - msg` is evaluated once at its definition.
- `extern` declares a symbol defined in another module, `global` exports one (ELF allows `global name:function`).
- `-l file` writes a listing; `-F format` selects the debug format and, from NASM 2.03.01, also enables `-g`.
- Linux x86-64 syscall numbers in the kernel table: `write` is 1 and `exit` is 60.

## Gotchas
- Floating-point constants need a period (`dd 1.0`); `dd 1` is an integer.
- Using `bin` format puts NASM in 16-bit mode unless you issue `BITS 32`/`BITS 64`.

## Self-check
Change the program to print a second line and exit with status 3.

## Checked
2026-11-08. Checked against the NASM manual chapters 2 (-l, -F), 3 (syntax, effective addresses, `$`/`$$`, local labels), 8 (EXTERN, GLOBAL) and 9 (bin, elf formats, sections), and the Linux x86-64 syscall table (write 1, exit 60). Removed: operand-order and "address versus contents" statements, the operand-size gotcha, the comment-swallowing gotcha, and the register-to-syscall argument comments, none of which the pages state.

Method: documentation only; no commands were run.
