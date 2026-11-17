---
id: computing-software.software-engineering.assembly.macho-format
name: macho-format
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, macho-format, asm-object-formats]
level: advanced
status: docs-checked
description: "Mach-O header fields, magic and CPU type constants, load commands, and the __TEXT and __DATA segments with their common sections."
sources:
  - https://raw.githubusercontent.com/apple-oss-distributions/xnu/main/EXTERNAL_HEADERS/mach-o/loader.h
  - https://raw.githubusercontent.com/apple-oss-distributions/xnu/main/osfmk/mach/machine.h
  - https://developer.apple.com/library/archive/documentation/Performance/Conceptual/CodeFootprint/Articles/MachOOverview.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Mach-O
**Goal:** read the structure of a Mach-O file for Apple platforms.

- A 64-bit Mach-O file starts with a `mach_header_64`: `magic` (`MH_MAGIC_64`, `0xfeedfacf`), `cputype`, `cpusubtype`, `filetype`, `ncmds` (number of load commands), `sizeofcmds`, `flags` and a reserved field. Load commands follow the header.
- CPU types: `CPU_TYPE_X86_64` is `CPU_TYPE_X86` (7) or-ed with `CPU_ARCH_ABI64` (`0x01000000`), giving `0x01000007`; `CPU_TYPE_ARM64` is `CPU_TYPE_ARM` (12) or-ed with the same flag, giving `0x0100000C`.
- Load command constants from `loader.h`: `LC_SYMTAB` is `0x2`, `LC_LOAD_DYLIB` is `0xc`, `LC_SEGMENT_64` is `0x19`, and `LC_MAIN` is `0x28 | LC_REQ_DYLD` (a replacement for `LC_UNIXTHREAD`).
- A Mach-O binary is organised into segments, and each segment holds one or more sections. Segment names are uppercase with leading double underscores (`__TEXT`), section names lowercase with leading double underscores (`__text`). Segments start on a page boundary; sections need not.
- `__TEXT` is read-only and holds executable code and constants: `__text` (machine code), `__const` (constant data), `__cstring` (literal string constants).
- `__DATA` is read/write: `__data` (initialized globals), `__bss` (uninitialized statics), `__common` (uninitialized external globals), plus dyld sections such as `__la_symbol_ptr` and `__nl_symbol_ptr`.

## Gotchas
- The Apple overview page is a retired archive document and says segments are multiples of 4096 bytes; page size on current hardware is not stated in these sources, so check the platform documentation before aligning segments.

## Self-check
From a hex dump of a 64-bit Mach-O file, read the magic and `cputype` and name the architecture.

## Checked
2026-11-08. Checked against Apple's xnu `loader.h` (header struct, `MH_MAGIC_64`, `LC_*` values, `SEG_TEXT`, `SEG_DATA`, `SECT_*`), xnu `machine.h` (`CPU_TYPE_*`, `CPU_ARCH_ABI64`) and the retired Apple Mach-O overview page (segment and section tables). Removed (no readable source): the arm64 assembly sample and clang/otool/nm commands, the leading-underscore symbol rule, the 16 KiB page-size claim, the `ld` and `-lSystem` advice, ELF-boilerplate and code-signing remarks. Replaced the LLVM and binutils root-page sources.

Method: documentation only; no commands were run.
