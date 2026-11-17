---
id: computing-software.software-engineering.assembly.pe-coff-format
name: pe-coff-format
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, pe-coff-format, asm-object-formats]
level: advanced
status: draft
description: "PE/COFF on Windows x64 and ARM64: DOS stub, PE signature, COFF header, optional header, sections like .text .rdata .pdata, imports and dumpbin inspection."
sources:
  - https://learn.microsoft.com/en-us/cpp/assembler/masm/microsoft-macro-assembler-reference
  - https://learn.microsoft.com/en-us/cpp/build/x64-software-conventions
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# PE/COFF
**Goal:** understand Windows executables and the objects that feed them.

- A PE file starts with a DOS header (`MZ`); its `e_lfanew` field points to the `PE\0\0` signature, followed by the COFF file header (machine type), the optional header, and the section table.
- Machine values: x64 is 0x8664, ARM64 is 0xAA64. The optional header magic for 64-bit images is 0x20B (PE32+).
- Common sections: `.text` code, `.rdata` read-only data and import tables, `.data`, `.pdata` and `.xdata` (unwind data), `.reloc` (base relocations), `.idata` (imports in some linkers).
- Data directories in the optional header locate imports, exports, exception tables, resources and base relocations.
- Assemblers (ml64, nasm `-f win64`, clang) emit COFF object files; the linker (`link.exe`, `lld-link`) produces the PE image.
```bat
dumpbin /headers prog.exe
dumpbin /disasm prog.exe
dumpbin /imports prog.exe
```
- x64 Windows C symbols have no underscore prefix.

## Gotchas
- ASLR requires the dynamic-base flag and base relocations; images without them load at a fixed base.
- Stripping `.pdata` of a non-leaf function breaks exception handling.

## Self-check
Dump headers of a tiny ml64 program and identify the entry point RVA.
