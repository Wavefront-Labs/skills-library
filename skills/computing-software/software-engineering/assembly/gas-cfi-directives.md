---
id: computing-software.software-engineering.assembly.gas-cfi-directives
name: gas-cfi-directives
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, gas-cfi-directives, asm-gas]
level: advanced
status: docs-checked
description: "Write .cfi_ directives in GAS so hand-written functions produce correct .eh_frame unwind data for debuggers, profilers and exceptions."
sources:
  - https://sourceware.org/binutils/docs/as/CFI-directives.html
  - https://sourceware.org/binutils/docs/as/AArch64-Directives.html
  - https://raw.githubusercontent.com/hjl-tools/x86-psABI/master/low-level-sys-info.tex
  - https://raw.githubusercontent.com/ARM-software/abi-aa/main/aadwarf64/aadwarf64.rst
  - https://sourceware.org/binutils/docs/binutils/readelf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# GAS CFI directives
**Goal:** keep stack unwinding accurate in assembly functions.

```gas
func:
        .cfi_startproc
        pushq   %rbp
        .cfi_def_cfa_offset 16          # CFA = rsp + 16 now
        .cfi_offset 6, -16              # rbp saved at CFA-16 (DWARF reg 6 = rbp)
        movq    %rsp, %rbp
        .cfi_def_cfa_register 6         # CFA now based on rbp
        ...
        popq    %rbp
        .cfi_def_cfa 7, 8               # back to rsp + 8
        ret
        .cfi_endproc
```
```gas
// AArch64
func:   .cfi_startproc
        stp     x29, x30, [sp, #-16]!
        .cfi_def_cfa_offset 16
        .cfi_offset 29, -16
        .cfi_offset 30, -8
        ...
        ldp     x29, x30, [sp], #16
        .cfi_restore 29
        .cfi_restore 30
        .cfi_def_cfa_offset 0
        ret
        .cfi_endproc
```
- `.cfi_startproc` opens a function's `.eh_frame` entry and `.cfi_endproc` closes and emits it; unless you pass `simple`, startproc also emits architecture-dependent initial CFI. By default `.eh_frame` is emitted; `.cfi_sections` can add `.debug_frame` or `.sframe`.
- The CFA is the canonical frame address. On AArch64 it is the value of `sp` at the call site in the previous frame; on x86-64 `(%rsp + 8)` is 16-byte aligned at function entry and the return address sits at `0(%rsp)`, so the CFA at entry is `rsp + 8`.
- `.cfi_def_cfa_offset` sets the absolute offset from the current CFA register; `.cfi_adjust_cfa_offset` adds a relative amount (handy after a `push`); `.cfi_offset reg, n` says the previous value of `reg` is saved at CFA + n; `.cfi_rel_offset` gives the offset from the current CFA register instead; `.cfi_restore reg` returns a register to its rule at function start.
- Use `.cfi_remember_state` before an early-return epilogue and `.cfi_restore_state` after it so code following the `ret` keeps the original rules.
- x86-64 DWARF numbers: rax 0, rdx 1, rcx 2, rbx 3, rsi 4, rdi 5, rbp 6, rsp 7, r8-r15 8-15, return address 16. AArch64: x0-x30 are 0-30 and sp is 31.
- A function that never moves the stack pointer needs only `.cfi_startproc`/`.cfi_endproc`.
- `.cfi_escape` emits arbitrary unwind bytes for opcodes GAS lacks. For return-address signing on AArch64, DWARF uses `DW_CFA_AARCH64_negate_ra_state`, and `.cfi_b_key_frame` marks frames signed with the B key.

## Gotchas
- Wrong CFI only shows when something unwinds (a crash, an exception, a profiler), so bugs can lurk until then.
- Register operands may be written as names (`%rbx`) or numbers; keep to one style per function.

## Self-check
Run `readelf --debug-dump=frames` (`-wf`) and confirm one FDE per function.

## Checked
2026-11-08. Confirmed against the GNU as manual (CFI directives, AArch64 Directives), the x86-64 psABI source (DWARF register number mapping, red zone, stack alignment), the AArch64 DWARF ABI (register numbers 0-30 and sp 31, CFA definition, negate_ra_state opcode) and the readelf manual (`--debug-dump=frames`, `-wf`). Removed: the claim that NASM has no CFI directives and the `.cfi_negate_ra_state` directive name (only the DWARF opcode is documented in these sources).
Method: documentation only; no commands were run.
