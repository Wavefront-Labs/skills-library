---
id: computing-software.software-engineering.assembly.aapcs64-callee-saved
name: aapcs64-callee-saved
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, aapcs64-callee-saved, asm-abi-aapcs64]
level: practitioner
status: docs-checked
description: "AAPCS64 register preservation: X19-X28 and X29 callee-saved, X30 link register, X16/X17 scratch, X18 platform register, low halves of V8-V15."
sources:
  - https://github.com/ARM-software/abi-aa/blob/main/aapcs64/aapcs64.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# AAPCS64 callee-saved registers
**Goal:** save exactly what the ABI requires.

- Callee-saved: `x19`-`x29` (`x29` is the frame pointer) and `sp`; of the SIMD/FP registers only `v8`-`v15`, and only their bottom 64 bits (`d8`-`d15`).
- `x30` (LR) receives the return address from `bl`/`blr`, so a function that calls another must save it.
- `x16` (IP0) and `x17` (IP1) are intra-procedure-call temporaries: a linker veneer or PLT code may change them between a call and the callee, so do not keep values in them across a call (they are ordinary caller-saved registers at other times).
- `x18` is the platform register, if the platform needs one; otherwise caller-saved. The standard advises portable hand-written assembly to avoid it entirely, and says treating it as callee-saved may not satisfy the platform.
- Caller-saved: `x0`-`x15`, `v0`-`v7`, `v16`-`v31`, and the upper bits of `v8`-`v15`.
```asm
func:
    stp  x29, x30, [sp, #-32]!
    mov  x29, sp
    stp  x19, x20, [sp, #16]     // we use x19, x20
    ...
    ldp  x19, x20, [sp, #16]
    ldp  x29, x30, [sp], #32
    ret
```
- The N, Z, C and V flags are undefined on entry to and return from a public interface.

## Gotchas
- Only the low 64 bits of `v8`-`v15` need saving; preserving the rest is the caller's job.
- SP mod 16 must be 0 whenever memory is accessed through SP, so frames are multiples of 16 bytes.

## Self-check
Use `x19` across a `bl` and confirm via a debugger that it survives the callee.

## Checked
2026-11-02. Checked against the AAPCS64 document (abi-aa, aapcs64.rst): general-purpose register table, notes on r16/r17/r18, the callee-saved rules for r19-r29, SP and v8-v15, the NZCV section and the stack constraints. Removed: the Apple/Windows/Android claims about `x18` (not in the standard), and the `str q8` remark.

Method: documentation only; no commands were run.
