---
id: computing-software.software-engineering.assembly.win64-arg-registers
name: win64-arg-registers
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, win64-arg-registers, asm-abi-win64]
level: practitioner
status: docs-checked
description: "Microsoft x64 calling convention: RCX RDX R8 R9 and XMM0-3 by position, by-reference aggregates, return registers and volatile versus non-volatile sets."
sources:
  - https://learn.microsoft.com/en-us/cpp/build/x64-calling-convention
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Microsoft x64 argument registers
**Goal:** call Windows API functions and write Win64-compatible assembly.

- The first four arguments go in `rcx, rdx, r8, r9` (integer or pointer) or `xmm0`-`xmm3` (float/double); the slot is by position, not by type, so `f(int, double)` uses `ecx` and `xmm1`. The unused register for that slot is ignored.
- Arguments beyond the first four go on the stack, right to left, after the shadow store, each keeping 8-byte alignment. Integer arguments in registers are right-justified, so the callee can ignore the upper bits.
- Any argument that is not 1, 2, 4 or 8 bytes is passed by reference; a single argument is never spread across registers. Structs and unions of 8, 16, 32 or 64 bits (and `__m64`) are passed as if integers of that size. `__m128`, arrays and strings are passed as a pointer to caller-allocated, 16-byte-aligned memory.
- Return: a scalar of up to 64 bits in `rax`; floats, doubles and vector types such as `__m128` in `xmm0`. Unused bits of the returned value are undefined.
- A user type that does not qualify for return in `rax` is returned through caller-allocated memory: the caller passes its pointer as the first argument (so the rest shift right, in `rcx` for the pointer) and the callee returns the same pointer in `rax`.
- Volatile: `rax, rcx, rdx, r8-r11, xmm0-xmm5`, and the upper portions of `ymm0-ymm15`. Non-volatile (must be saved and restored by a function that uses them): `rbx, rbp, rdi, rsi, rsp, r12-r15, xmm6-xmm15`.
- Varargs and unprototyped functions: a floating-point value must be in both its XMM register and the matching integer register.
- The x87 stack is unused for arguments; treat it as volatile across calls. The x87 control word and the non-status part of MXCSR (bits 6-15) are non-volatile.

## Gotchas
- A callee that needs the register arguments in memory must dump them to the shadow space itself.
- A call with a hidden return pointer shifts every real argument one slot to the right.

## Self-check
Write the argument registers for `f(int a, double b, int c, float d, int e)` and for a function returning a 12-byte struct.

## Checked
2026-11-08. Checked against the Microsoft Learn x64 calling convention page (parameter passing table, varargs, return values, caller/callee saved registers, FPCSR/MXCSR). Removed: the `rdi`/`rsi` SysV porting gotcha, the claim that only the low 128 bits of `xmm6-xmm15` are preserved, and the MessageBoxA self-check, none of which the page states.

Method: documentation only; no commands were run.
