---
id: computing-software.software-engineering.assembly.elf-sections-segments
name: elf-sections-segments
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, elf-sections-segments, asm-object-formats]
level: practitioner
status: docs-checked
description: "ELF layout: section headers versus program headers (segments), common section names and flags, PT_LOAD and PT_GNU_STACK, and inspecting with readelf."
sources:
  - https://man7.org/linux/man-pages/man5/elf.5.html
  - https://sourceware.org/binutils/docs/binutils/readelf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ELF sections and segments
**Goal:** read an ELF file the way the linker and loader do.

- Section header table: sections such as `.text`, `.rodata`, `.data`, `.bss`, `.symtab`, `.strtab`, `.rela.text`. Each section header carries a type (`sh_type`) and flag bits (`SHF_ALLOC`, `SHF_WRITE`, `SHF_EXECINSTR`).
- `.bss` holds uninitialized data and is type `SHT_NOBITS`: it can have a nonzero size but occupies no space in the file. Its attributes are `SHF_ALLOC` and `SHF_WRITE`.
- Program header table: segments, each with a `p_type`. `PT_LOAD` is a loadable segment described by `p_filesz` and `p_memsz`; if `p_memsz` is larger, the extra bytes are zero. `PT_DYNAMIC` carries dynamic linking information, `PT_INTERP` the interpreter pathname (at most once, before any loadable entry), `PT_NOTE` the notes, and `PT_GNU_STACK` is a GNU extension the Linux kernel uses to control the stack state through `p_flags`.
```sh
readelf -h prog        # ELF file header (--file-header)
readelf -S prog        # section headers (--sections)
readelf -l prog        # program headers (--segments)
readelf -s prog        # symbol table (--syms)
```
- The ELF header's `e_entry` field is the entry point address.
- `.note.GNU-stack` is a section in Linux object files for declaring stack attributes; if it carries `SHF_EXECINSTR`, the GNU linker treats the object as requiring an executable stack.

## Gotchas
- A section is what the linker sees; a segment is what the loader maps. One `PT_LOAD` segment normally covers several sections.

## Self-check
Run `readelf -S` and `readelf -l` on a small binary and find which sections fall inside each `PT_LOAD` segment.

## Checked
2026-11-08. Checked against the Linux elf(5) manual page (section names, `SHT_NOBITS` and `.bss`, `PT_LOAD`, `PT_DYNAMIC`, `PT_INTERP`, `PT_NOTE`, `PT_GNU_STACK`, `e_entry`, `.note.GNU-stack`) and the binutils readelf page (`-h`, `-S`, `-l`, `-s` and their long forms). Removed (not on these pages or unreadable): `.eh_frame`, `PT_TLS`, `PT_GNU_RELRO`, the flag-letter key in `readelf -S`, the typical three-`PT_LOAD` layout, PIE random base, the NASM custom-section lines, `--gc-sections` and the W^X remarks. Replaced the root-page sources; the linuxfoundation ELF PDF was unreadable as text.

Method: documentation only; no commands were run.
