---
id: computing-software.software-engineering.assembly.adrp-add-pc-relative
name: adrp-add-pc-relative
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, adrp-add-pc-relative, asm-arm64-loadstore]
level: practitioner
status: docs-checked
description: "Take addresses of symbols on AArch64 with ADRP plus ADD or LDR, with ELF and GOT relocation syntax and the 4 GiB range."
sources:
  - https://sourceware.org/binutils/docs/as/AArch64_002dRelocations.html
  - https://github.com/ARM-software/abi-aa/blob/main/aaelf64/aaelf64.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ADRP + ADD / LDR PC-relative addressing
**Goal:** reference globals in position-independent code.

- `adrp xN, sym` produces a page-relative address of `sym`; the GNU assembler documents it as 33-bit (+/-4GB) pc-relative addressing, and the paired instruction supplies the low 12 bits.
```asm
// ELF (GNU as / clang)
adrp x0, msg
add  x0, x0, :lo12:msg           // x0 = &msg
adrp x1, counter
ldr  x1, [x1, :lo12:counter]     // load directly
// GOT-indirect for external/preemptible symbols
adrp x2, :got:ext_sym
ldr  x2, [x2, :got_lo12:ext_sym]
```
- Relocations: `adrp x0, sym` is `R_AARCH64_ADR_PREL_PG_HI21` (checked against -2^32 <= X < 2^32), `add ... :lo12:` is `R_AARCH64_ADD_ABS_LO12_NC`, `adrp x0, :got:sym` is `R_AARCH64_ADR_GOT_PAGE` and `ldr ... :got_lo12:` is `R_AARCH64_LD64_GOT_LO12_NC`. For loads and stores, the `LDST*_ABS_LO12_NC` relocations (e.g. `R_AARCH64_LDST64_ABS_LO12_NC`, bits [11:3]) scale the low 12 bits by the access size, and the linker should check the value is aligned to the datum size.
- In the GNU assembler `:pg_hi21:` is optional: `adrp x0, foo` is equivalent to `adrp x0, :pg_hi21:foo`. The GNU manual also shows `adrp x0, foo` with `ldr x0, [x0, #:lo12:foo]`.

## Gotchas
- The relocation operators are assembler syntax: the Mach-O spellings (`@PAGE`, `@PAGEOFF`, `@GOTPAGE`) and the ranges of `adr` and `ldr =value` were not in the sources read and are not covered here.

## Self-check
Disassemble with relocations (`objdump -dr`) and find the two paired relocations per symbol.

## Checked
2026-11-02. Checked against the GNU as AArch64 "Relocations" page (`:pg_hi21:`, `:lo12:`, 33-bit +/-4GB, ldr form) and AAELF64 (relocation tables 275/286/299, GOT and relaxation examples with the relocation names). Removed: Mach-O `@PAGE` operators, `adr` +/-1 MiB range, the `ldr =value` pseudo-instruction and literal pool remarks, and the adjacency advice. Fixed: the load example used `w1` with a `counter`; the register width must match the relocation chosen, so it now uses `x1` (64-bit load, `LDST64`).

Method: documentation only; no commands were run.
