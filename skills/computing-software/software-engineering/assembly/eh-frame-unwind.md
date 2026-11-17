---
id: computing-software.software-engineering.assembly.eh-frame-unwind
name: eh-frame-unwind
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, eh-frame-unwind, asm-debug-info]
level: advanced
status: docs-checked
description: ".eh_frame unwind tables from GAS CFI directives: .cfi_sections defaults, startproc/endproc, register save rules and dumping frames with readelf."
sources:
  - https://sourceware.org/binutils/docs/as/CFI-directives.html
  - https://sourceware.org/binutils/docs/binutils/readelf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# .eh_frame unwinding
**Goal:** keep unwinding working through hand-written assembly functions.

- GAS CFI directives emit call-frame information. By default (`.cfi_sections .eh_frame`) they produce `.eh_frame`; `.cfi_sections .eh_frame, .debug_frame` emits both, and `.sframe` is also accepted. `.cfi_sections` can be repeated only until CFI generation has started.
- `.cfi_startproc` begins every function that should have an `.eh_frame` entry and `.cfi_endproc` closes and emits it. Unless `.cfi_startproc simple` is used, it also emits architecture-dependent initial CFI instructions. A function without these directives gets no entry.
- Describe stack changes as you go: `.cfi_def_cfa register, offset` (CFA = register + offset), `.cfi_def_cfa_offset offset` (absolute), `.cfi_adjust_cfa_offset offset` (relative), `.cfi_def_cfa_register register`.
- Describe saved registers: `.cfi_offset register, offset` (saved at offset from the CFA), `.cfi_rel_offset register, offset` (offset from the current CFA register, often easier because the number matches the code), `.cfi_restore register`, `.cfi_remember_state` and `.cfi_restore_state` around early-return paths.
```gas
func:
        .cfi_startproc
        pushq %rbx
        .cfi_adjust_cfa_offset 8
        .cfi_rel_offset %rbx, 0
        popq  %rbx
        .cfi_adjust_cfa_offset -8
        .cfi_restore %rbx
        ret
        .cfi_endproc
```
- Inspect with `readelf --debug-dump=frames prog` (or `-wf`). `readelf --unwind` supports only IA64 and ARM tables; for other architectures the manual suggests `--debug-dump=frames` or `--debug-dump=frames-interp` instead.
- `.cfi_signal_frame` marks a signal trampoline, `.cfi_undefined register` says a register's previous value cannot be restored, and `.cfi_escape` adds arbitrary bytes to the unwind info.

## Gotchas
- Directives that do not match the real code (for example after reordering pushes) give wrong unwind rules without any assembler error.
- `.cfi_sections` after CFI generation has started is an error.

## Self-check
Assemble the example, run `readelf --debug-dump=frames` and confirm one FDE for `func` whose CFA rule changes after the push.

## Checked
Method: docs-checked 2026-11-09 against the GNU as page CFI directives and the readelf page (debug-dump and unwind options). Dropped unconfirmed claims about which tools consume `.eh_frame`, GDB fallback heuristics, compiler flags and the Windows and macOS equivalents.
