---
id: computing-software.software-engineering.assembly.masm-proc-frame
name: masm-proc-frame
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, masm-proc-frame, asm-masm]
level: advanced
status: docs-checked
description: "MASM x64 PROC FRAME with .PUSHREG, .ALLOCSTACK, .SETFRAME and .ENDPROLOG to generate unwind data, plus the epilog rules."
sources:
  - https://learn.microsoft.com/en-us/cpp/assembler/masm/proc
  - https://learn.microsoft.com/en-us/cpp/assembler/masm/dot-pushreg
  - https://learn.microsoft.com/en-us/cpp/assembler/masm/dot-allocstack
  - https://learn.microsoft.com/en-us/cpp/assembler/masm/dot-setframe
  - https://learn.microsoft.com/en-us/cpp/assembler/masm/dot-endprolog
  - https://learn.microsoft.com/en-us/cpp/assembler/masm/dot-savereg
  - https://learn.microsoft.com/en-us/cpp/assembler/masm/dot-savexmm128
  - https://learn.microsoft.com/en-us/cpp/build/prolog-and-epilog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# PROC FRAME and unwind directives
**Goal:** generate correct `.pdata`/`.xdata` for non-leaf functions in MASM (ml64).

```masm
frmex2 PROC FRAME
    push rbp
.pushreg rbp
    sub  rsp, 010h
.allocstack 010h
    mov  rbp, rsp
.setframe rbp, 0
.endprolog
    ; modify rsp outside the prologue (similar to alloca) is allowed
    ; because a frame pointer is set
    add  rsp, 010h
    pop  rbp
    ret
frmex2 ENDP
```
- `PROC FRAME` is valid only with ml64.exe; it makes MASM generate a function table entry in `.pdata` and unwind information in `.xdata`. `FRAME` must be followed by `.ENDPROLOG`; `FRAME:ehandler-address` names an exception handler.
- The prologue runs from `PROC FRAME` to `.ENDPROLOG`; using a prologue directive outside that region is an error.
- The directives generate unwind metadata but no code. Precede each one with the instruction it describes (unwind version 1) and keep them in agreement, for example by wrapping both in a macro. (Under the experimental `/unwindv3` the directive goes before the instruction.)
- `.PUSHREG reg` makes a `UWOP_PUSH_NONVOL` entry; `.ALLOCSTACK size` picks `UWOP_ALLOC_SMALL` or `UWOP_ALLOC_LARGE` and needs a multiple of 8; `.SETFRAME reg, offset` needs an offset that is a multiple of 16 and at most 240.
- `.SAVEREG reg, offset` records a register saved in the frame (`UWOP_SAVE_NONVOL`); `.SAVEXMM128 xmm, offset` records an XMM save and the offset must be a multiple of 16.
- Epilog rules (from the x64 prolog and epilog page): `add rsp, constant` or `lea rsp, constant[FPReg]`, then zero or more 8-byte pops, then a `ret` or a restricted `jmp`. Nothing else may appear in an epilog, including loading the return value. Without a frame pointer the epilog must use `add rsp, constant`, not `lea`.
- The first use of a non-volatile register in the prolog must be to save it; saving by `push`/`mov` before the fixed allocation is preferred. A fixed allocation of one page (4096 bytes) or more must call `__chkstk` first.

## Gotchas
- A directive that does not match the actual instruction before it gives wrong unwind data.
- Nothing may be scheduled inside an epilog, including loading the return value.

## Self-check
Add `.savereg` for a register saved with a `mov` into the frame, and confirm every directive follows its instruction.

## Checked
2026-11-08. Checked against the Microsoft Learn pages for PROC (MASM), .PUSHREG, .ALLOCSTACK, .SETFRAME, .ENDPROLOG, .SAVEREG, .SAVEXMM128 and x64 prolog and epilog. Removed: the claim that non-leaf functions without FRAME fail fast-fail checks, the debugger-related gotcha and the 16-byte alignment arithmetic in the original example.

Method: documentation only; no commands were run.
