---
id: computing-software.software-engineering.assembly.asm-modular-source
name: asm-modular-source
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, asm-modular-source, asm-project]
level: practitioner
status: docs-checked
description: "Organise assembly projects: NASM %include and macros, GAS .include, per-function sections with ld --gc-sections, include paths and local labels."
sources:
  - https://www.nasm.us/doc/nasm02.html
  - https://sourceware.org/binutils/docs/as/Include.html
  - https://sourceware.org/binutils/docs/as/Section.html
  - https://sourceware.org/binutils/docs/as/Type.html
  - https://sourceware.org/binutils/docs/as/Symbol-Names.html
  - https://sourceware.org/binutils/docs/as/Overview.html
  - https://sourceware.org/binutils/docs/ld/Options.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Modular source with include and macros
**Goal:** split code into maintainable files.

```nasm
; common.inc  (NASM)
%define SYS_write 1
%macro FUNC 1
    global %1
    %1:
%endmacro
; strutil.asm
%include "common.inc"
section .text
FUNC my_strlen
    ; in: rdi = C string   out: rax = length   clobbers: rcx
    ret
```
```gas
        .include "common.inc"
        .section .text.my_strlen,"ax",@progbits
        .globl my_strlen
        .type my_strlen, @function
my_strlen:
```
- GAS `.include "file"` assembles the file as if it followed that point; quotation marks are required, and `as -I dir` adds to the search list. NASM `%include "file"` searches the current directory and any `-i dir` (also spelled `-I`) directories; `-p file` pre-includes a file as if `%include` were first in the source, and `-dFOO=100` is an alternative to a `%define`.
- Since NASM 2.14 the trailing path separator on an `-i` directory is always added (`-ifoo` means `-ifoo/`); older versions needed it written out.
- One function per section lets the linker drop unused code: `ld --gc-sections` removes unused input sections, keeping the section with the entry symbol, sections with symbols undefined on the command line or referenced by dynamic objects, and anything they reference through relocations. In a shared library every visible symbol is assumed referenced.
- GAS `.section name,"flags",@type`: flag `a` allocatable, `x` executable, `w` writable; `@progbits` means the section contains data. `.type name, @function` marks an ELF function symbol (the `STT_FUNC` spelling is accepted on all architectures where `@` is a comment character).
- Local helpers: on ELF, GAS treats symbols starting with `.L` as internal; they are normally not saved in object files and so are invisible when debugging. Omit `global` / `.globl` to keep a symbol private to the object.
- Document arguments, return value and clobbered registers in a comment block per function, and keep such notes next to macros, which hide clobbers. Assembly has no namespaces, so use a module prefix in names.

## Gotchas
- `--gc-sections` has no effect on code that shares a single `.text` section.
- Symbols in a shared library are all treated as referenced for garbage collection.

## Self-check
Move a routine into its own section, link with `--gc-sections --print-gc-sections`, and confirm the unused section is reported removed.

## Checked
Method: docs-checked 2026-11-09 against NASM manual chapter 2 (-i, -p, -d options), the GNU as pages Include, Section, Type, Symbol Names and Overview (-I), and the ld options page (--gc-sections). Dropped the `-ffunction-sections` equivalence, the MASM include form and the uppercase `.S` preprocessor note as unconfirmed. Corrected the earlier claim that NASM needs a trailing slash on `-I` directories.
