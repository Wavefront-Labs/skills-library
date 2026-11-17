---
id: computing-software.software-engineering.assembly.win64-unwind-seh
name: win64-unwind-seh
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, win64-unwind-seh, asm-abi-win64]
level: sme
status: docs-checked
description: "Windows x64 stack unwinding: pdata RUNTIME_FUNCTION and xdata UNWIND_INFO, MASM PROC FRAME directives, and rules for prologs and epilogs."
sources:
  - https://learn.microsoft.com/en-us/cpp/build/exception-handling-x64
  - https://learn.microsoft.com/en-us/cpp/build/prolog-and-epilog
  - https://learn.microsoft.com/en-us/cpp/build/x64-calling-convention
  - https://learn.microsoft.com/en-us/cpp/assembler/masm/proc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Unwind info, prologs and SEH (Win64)
**Goal:** make a non-leaf assembly function unwindable so exceptions and debuggers work.

- Table-based exception handling needs a `RUNTIME_FUNCTION` entry for every function that allocates stack space or calls another function (non-leaf). Each entry is three `ULONG`s: function start, function end and unwind info address, all image-relative (32-bit offsets from the image start). They are sorted and placed in the `.pdata` section of a PE32+ image, and the structure must be DWORD aligned.
- JIT or other dynamically generated code must register its table with `RtlInstallFunctionTableCallback` or `RtlAddFunctionTable`; otherwise exception handling and debugging are unreliable.
- `UNWIND_INFO` (in `.xdata`) holds version, flags, size of prolog, count of unwind codes, frame register and scaled frame offset, then an unwind code array, then either an exception handler (address plus optional language-specific data) or chained unwind info. The frame register is set to `RSP + 16 * scaled offset`, so offsets run from 0 to 240.
- Flags: `UNW_FLAG_EHANDLER` (exception handler, such as C `__try`), `UNW_FLAG_UHANDLER` (termination handler, such as destructors and `__finally`) and `UNW_FLAG_CHAININFO` (chained info; the other two must then be clear).
- Each `UNWIND_CODE` records the offset in the prolog (end of the instruction, plus 1), an operation code and operation info. The array is sorted in descending order of prolog offset and always holds an even number of entries.
- Because of the epilog constraints, `UWOP_PUSH_NONVOL` codes must appear first in the prolog and last in the unwind array.
- MASM generates this data from directives:
```masm
foo PROC FRAME
    push rbx
.pushreg rbx
    sub  rsp, 32
.allocstack 32
.endprolog
    ; ...
    add  rsp, 32
    pop  rbx
    ret
foo ENDP
```
- A prolog may save argument registers to their home addresses, push non-volatile registers, allocate the fixed stack area and optionally set a frame pointer. The unwind data must describe all of it. Epilogs must match a strict pattern (`add rsp, const` or `lea rsp, const[FPReg]`, pops, `ret` or a restricted `jmp`) so the unwinder can detect them by scanning forward.
- The stack pointer must stay 16-byte aligned outside prologs and epilogs, except in leaf functions. A leaf function changes no non-volatile registers (including RSP) and needs no pdata or xdata.

## Gotchas
- The unwind data covers only what the directives describe; add a matching directive for every prolog action.
- Registers like the x87 control word and parts of MXCSR are non-volatile but have no unwind descriptor, so exception-safe code that changes them must restore them in a finalizer (`__finally` or a destructor).

## Self-check
Write the `.pdata` fields for a function and name the unwind code needed for `push rbx` followed by `sub rsp, 32`.

## Checked
2026-11-08. Checked against the Microsoft Learn pages x64 exception handling (RUNTIME_FUNCTION, UNWIND_INFO, UNWIND_CODE), x64 prolog and epilog, x64 calling convention (Unwindability, FPCSR and MXCSR) and PROC (MASM). Removed: the GNU as `.seh_*` directives (the GAS page was unreadable), the 255-byte prologue limit, the NASM-has-no-unwind-directives remark and the claim that a fault without unwind info crashes the process instead of raising a structured exception.

Method: documentation only; no commands were run.
