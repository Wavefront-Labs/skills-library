---
id: computing-software.software-engineering.assembly.frame-pointer-chains
name: frame-pointer-chains
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, frame-pointer-chains, asm-stack-frames]
level: advanced
status: docs-checked
description: "Walk the frame pointer chain on x86-64 (RBP) and AArch64 (X29) for cheap backtraces, with layout and caveats."
sources:
  - https://gitlab.com/x86-psABIs/x86-64-ABI
  - https://github.com/ARM-software/abi-aa/blob/main/aapcs64/aapcs64.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Frame-pointer chains and backtraces
**Goal:** unwind stacks without DWARF when every function keeps a frame pointer.

- x86-64: with a base pointer, `0(%rbp)` holds the previous `%rbp` value and `8(%rbp)` the return address; the first stacked argument is at `16(%rbp)` (System V psABI stack-frame figure).
- AArch64: conforming code builds a linked list of frame records, each two 64-bit values. The frame pointer `x29` points at the innermost record; its lowest-addressed double-word points to the previous record and the highest holds the link register value on entry. So the previous `x29` is at `[x29]` and the return address at `[x29+8]`.
- AArch64 platforms choose how strictly records are maintained: always valid (small leaf routines that leave the link register alone may skip the record), always valid with any routine allowed to skip, or the frame pointer used as a general callee-saved register. During frame construction or destruction `x29` briefly points at the caller's record.
```nasm
; fill buf[0..n) with return addresses; rdi = buf, esi = n  -> eax = count
backtrace:
    xor  eax, eax
    mov  rdx, rbp
.next:
    test rdx, rdx
    jz   .done
    cmp  eax, esi
    jae  .done
    mov  rcx, [rdx + 8]       ; return address
    mov  [rdi + rax*8], rcx
    inc  eax
    mov  rdx, [rdx]           ; caller's frame
    jmp  .next
.done: ret
```
- The psABI says the content of `%rbp` is unspecified at process start, and that the user code should mark the deepest stack frame by setting the frame pointer to zero; the loop above stops on a null frame pointer for that reason.

## Gotchas
- `%rbp` is only a frame pointer by convention (the psABI calls it callee-saved, optionally used as a frame pointer); code or assembly routines that use it as a general register or skip the prologue break the chain.
- Validate pointers before dereferencing in signal-time unwinders.
- Compiler flags to keep frame pointers and the profiler options that rely on them are not stated by the sources read here; check your compiler and profiler manuals.

## Self-check
Call `backtrace` from a three-deep call chain built with frame pointers and print the addresses with `addr2line`.

## Checked
2026-11-02. Checked against the System V x86-64 psABI (low-level-sys-info: stack frame figure, register usage table, process initialisation note on `%rbp`) and AAPCS64 (abi-aa: "The Frame Pointer" section). Removed: `-fno-omit-frame-pointer` / `-fomit-frame-pointer` default claims, `perf record --call-graph fp`, and the claim that some distributions enable frame pointers by default (none of these pages were read).

Method: documentation only; no commands were run.
