---
id: computing-software.software-engineering.assembly.relocations
name: relocations
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, relocations, asm-linking]
level: advanced
status: docs-checked
description: "ELF relocation types for x86-64 and AArch64 produced by assemblers, how to read them with readelf and objdump, and common linker errors."
sources:
  - https://gitlab.com/x86-psABIs/x86-64-ABI
  - https://github.com/ARM-software/abi-aa/blob/main/aaelf64/aaelf64.rst
  - https://sourceware.org/binutils/docs/binutils/readelf.html
  - https://sourceware.org/binutils/docs/binutils/objdump.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Relocation types
**Goal:** understand what the assembler leaves for the linker to fix.

- A relocation patches a field with a value computed from the symbol value `S`, an addend `A`, and sometimes the place `P`, a GOT offset `G`, or the PLT address `L`. The x86-64 LP64 ABI uses only `Elf64_Rela` entries, which carry an explicit addend in `r_addend`.
- x86-64 (System V psABI relocation table): `R_X86_64_64` (word64, `S+A`), `R_X86_64_PC32` (word32, `S+A-P`), `R_X86_64_PLT32` (word32, `L+A-P`), `R_X86_64_GOTPCREL` (word32, `G+GOT+A-P`, the distance from the place to the GOT slot), `R_X86_64_32` and `R_X86_64_32S` (word32, `S+A`; both truncate the generated value, so they are absolute addresses).
- AArch64 (AAELF64): `R_AARCH64_CALL26` (283, `BL`) and `R_AARCH64_JUMP26` (282, `B`) check -2^27 <= X < 2^27, a range of +/-128 MiB; `R_AARCH64_ADR_PREL_PG_HI21` (275, an ADRP immediate, `Page(S+A)-Page(P)`, checked against +/-2^32); `R_AARCH64_LDST64_ABS_LO12_NC` (286, bits [11:3] of X for a 64-bit load/store, no overflow check); `R_AARCH64_ABS64` (257, `S+A`, 64-bit); the GOT forms `R_AARCH64_ADR_GOT_PAGE` (311) and `R_AARCH64_LD64_GOT_LO12_NC`; `R_AARCH64_ADD_ABS_LO12_NC` pairs with ADRP for `:lo12:`.
```sh
readelf -r prog.o              # relocation table (--relocs)
objdump -dr prog.o             # relocations interspersed with the disassembly (-r with -d)
```
- A call to a function from x86-64 code is expressed with a `R_X86_64_PLT32` relocation (the psABI shows `foo@PLT(%rip)` assembling to it).
- AAELF64 lists a target outside the +/-128MB span of the branch as a failure case; AAPCS64 says a linker may insert a veneer (using `x16`/`x17`) between caller and callee when a branch cannot reach.

## Gotchas
- Use RIP-relative or ADRP forms rather than absolute immediates in position-independent code; `R_X86_64_32`/`32S` truncate to 32 bits.
- The exact text of linker errors ("relocation truncated to fit", "can not be used when making a PIE object") was not checked against the ld manual; read them as out-of-range or absolute-in-PIC diagnostics and look up the wording for your linker.

## Self-check
Assemble a function call and an address load and name the relocation on each with `objdump -dr`.

## Checked
2026-11-02. Checked against the System V x86-64 psABI (object-files: relocation types table, GOTPCREL notes, Elf64_Rela statement), AAELF64 (static relocation tables, ADRP/ADD/GOT examples, branch range text), and the binutils readelf (`-r`/`--relocs`) and objdump (`-r`/`--reloc`, interspersed with `-d`) manuals. Removed: the "older binutils PC32 with addend -4" remark, the claim that PC32 is for RIP-relative data, the exact `ld` error strings and the `printf`/`lea` self-check wording.

Method: documentation only; no commands were run.
