---
id: computing-software.software-engineering.assembly.rip-relative
name: rip-relative
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, rip-relative, asm-x86-addressing]
level: practitioner
status: docs-checked
description: "RIP-relative addressing in NASM x86-64: REL and ABS keywords, DEFAULT REL, FS/GS exceptions, and splitting indexed table jumps with lea."
sources:
  - https://www.nasm.us/doc/nasm03.html
  - https://www.nasm.us/doc/nasm08.html
  - https://www.nasm.us/doc/nasm09.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# RIP-relative addressing
**Goal:** reference globals without absolute addresses so code is position-independent.

- In 64-bit mode NASM generates absolute addresses by default. The `REL` keyword makes an address RIP-relative and `ABS` overrides it.
```nasm
default rel                       ; make registerless [sym] RIP-relative from here on
section .rodata
msg: db "hi", 10
section .text
lea rsi, [rel msg]                ; explicit form, works without default rel
mov eax, [rel counter]
```
- `DEFAULT REL` affects registerless memory references in 64-bit mode, except those with an `FS` or `GS` segment override, because those registers are usually thread pointers. To make them relative too, write for example `DEFAULT REL, FS:ABS, GS:REL` (here `FS` stays absolute and everything else, `GS` included, is RIP-relative). `DEFAULT ABS` turns the setting off. The manual notes `DEFAULT REL` is likely to become NASM's default in a future version, so say `DEFAULT ABS` explicitly if code must avoid relative offsets.
- Indexed table jumps: a form like `jmp qword [table+rax*8]` has a registerless base and, in a Win64 context, the linker refuses it with an ADDR32 relocation error. Load the table address RIP-relatively first, then index from the register:
```nasm
lea rbx, [rel table]
jmp qword [rbx+rax*8]
```
- When the table holds absolute addresses in a DLL, loader relocations make those pages private to the process; the manual's remedy is to store `wrt ..imagebase` offsets and `add rbx,[rbx+rax*8]` before jumping.

## Gotchas
- Without `DEFAULT REL` or an explicit `rel`, `[sym]` in 64-bit NASM is an absolute reference and may not link in position-independent output.
- `wrt ..imagebase` offsets are 32-bit values (`dd`, not `dq`).

## Self-check
Assemble twice, with and without `default rel`, and compare the `objdump -dr` disassembly of the two objects.

## Checked
Method: docs-checked 2026-11-09 against NASM manual chapter 3 (REL and ABS in effective addresses), chapter 8 (section 8.2.1 DEFAULT REL) and chapter 9 (section 9.7.1 Win64 position-independent code). Dropped the Intel displacement range, GAS syntax and the PIE linking and GOT claims, which these pages do not confirm.
