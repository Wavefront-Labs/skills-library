---
id: computing-software.software-engineering.compiler-construction.elf-sections-symbols-relocs
name: elf-sections-symbols-relocs
category: computing-software
field: software-engineering
product: compiler-construction
tags: [compiler-construction, elf-sections, symbol-table, relocation-types, elf-format, relocations, linker, compilers, interpreters, language-implementation]
level: practitioner
status: draft
description: "Binary anatomy"
sources: ["https://craftinginterpreters.com/", "https://llvm.org/docs/", "https://llvm.org/docs/tutorial/", "https://mlir.llvm.org/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ELF, symbols and relocations

Goal: read object files.
- `readelf -S -s -r a.o`, `objdump -dr a.o`; sections `.text`, `.data`, `.rodata`, `.bss`; relocations patched by the linker (R_X86_64_PC32, PLT32).
- Symbol binding (local/global/weak), visibility.
- Mach-O and PE have analogous structures.
Verify: you can explain each relocation in a small object file.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
