---
id: computing-software.software-engineering.assembly.win64-shadow-space
name: win64-shadow-space
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, win64-shadow-space, asm-abi-win64]
level: practitioner
status: docs-checked
description: "Microsoft x64 shadow (home) space: the four-register parameter area the caller must reserve, stack alignment rules, and where stack arguments sit."
sources:
  - https://learn.microsoft.com/en-us/cpp/build/x64-calling-convention
  - https://learn.microsoft.com/en-us/cpp/build/stack-usage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Shadow space and stack alignment (Win64)
**Goal:** keep the stack legal for every call.

- The caller must always allocate enough space for four register parameters (four 8-byte entries, 32 bytes), even if the callee takes fewer arguments. This area sits at the bottom of the stack, adjacent to the return address during any call, and stack arguments follow it.
- The parameter area holds at least four entries and always enough for the parameters of any function the caller may call, so allocate the largest outgoing area once in the prolog.
- Home addresses exist so a contiguous area is available if the callee takes the address of an argument or the argument list (`va_list`). The callee is responsible for dumping register parameters there if needed.
- The four locations are effectively owned by the callee and may be used for other purposes, so the caller must not keep information there across a call.
- The stack is kept 16-byte aligned except within a prolog (for example right after the return address is pushed). A frame function that calls nothing need not align it, and a leaf function may leave it unaligned.
- With 8 bytes of return address plus the 32-byte shadow store, the fifth argument is at `[rsp+0x28]` on entry to the callee. A function that has pushed only the return address therefore needs another 8 bytes (for example `sub rsp, 40` with no other locals) to restore alignment before calling.
```nasm
; caller with no locals, calls a function taking <= 4 args
sub  rsp, 40        ; 32 shadow store + 8 to realign after the return address
; load rcx, rdx, r8, r9 here, then call
add  rsp, 40
```
- If a function uses `alloca`, a non-volatile register must be the frame pointer, and calls from the same caller may then use different home addresses.

## Gotchas
- If the caller skips the shadow space, the callee's use of those four slots overwrites whatever lies there.
- Memory beyond the current `rsp` is volatile (the OS or a debugger may overwrite it), so set `rsp` before writing to a frame.

## Self-check
For a function with 40 bytes of locals that calls a 6-argument function, compute the `sub rsp, N` that keeps alignment.

## Checked
2026-11-08. Checked against the Microsoft Learn x64 calling convention page and x64 stack usage page. Removed: the NASM ExitProcess program, the claim that misalignment crashes in SSE stores, and the `-f win64` build line, none of which the pages state. The `[rsp+0x28]` offset and the `sub rsp, 40` example are arithmetic from the stated layout (return address plus 32-byte store).

Method: documentation only; no commands were run.
