---
id: computing-software.software-engineering.assembly.sysv-struct-passing
name: sysv-struct-passing
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, sysv-struct-passing, asm-abi-sysv]
level: sme
status: draft
description: "System V AMD64 aggregate classification into INTEGER, SSE and MEMORY eightbytes, passing small structs in registers and returning large ones via hidden pointer."
sources:
  - https://gitlab.com/x86-psABIs/x86-64-ABI
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Struct classification and passing (SysV)
**Goal:** predict where a struct argument or return value lives.

- Structs up to 16 bytes are split into eightbytes; each eightbyte is classed INTEGER (any integer/pointer field), SSE (only float/double), X87 (`long double`) or MEMORY.
- If every eightbyte can get a register of its class, the struct is passed in registers; otherwise the whole struct goes on the stack.
- Structs larger than 16 bytes (or with unaligned fields) are MEMORY: copied onto the stack for arguments.
```
struct P { double x, y; }     -> xmm0, xmm1
struct Q { long a; double b; }-> rdi, xmm0
struct R { int a, b, c; }     -> rdi (a,b), rsi (c)
struct S { long a, b, c; }    -> MEMORY (24 bytes) on the stack
```
- Returned MEMORY structs: the caller passes a hidden pointer in `rdi` (shifting real arguments by one register) and the callee returns that pointer in `rax`.
- Returned register structs use `rax`/`rdx` for INTEGER eightbytes and `xmm0`/`xmm1` for SSE, assigned in order.
- Classification also considers C++ non-trivial copy/destructor, which forces passing by invisible reference (Itanium C++ ABI).

## Gotchas
- If registers run out midway, the struct moves entirely to the stack; it is not split.
- Packed structs with misaligned fields are MEMORY.

## Self-check
Compile the four examples in C and check the generated assembly against the table.
