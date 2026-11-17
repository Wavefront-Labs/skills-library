---
id: computing-software.software-engineering.assembly.gas-directives-sections
name: gas-directives-sections
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, gas-directives-sections, asm-gas]
level: practitioner
status: docs-checked
description: "Common GNU as directives: symbol visibility, size, data definitions, alignment, BSS and common reservations, and the alignment-argument trap."
sources:
  - https://sourceware.org/binutils/docs/as/Align.html
  - https://sourceware.org/binutils/docs/as/Comm.html
  - https://sourceware.org/binutils/docs/as/Lcomm.html
  - https://sourceware.org/binutils/docs/as/Local.html
  - https://sourceware.org/binutils/docs/as/Hidden.html
  - https://sourceware.org/binutils/docs/as/Size.html
  - https://sourceware.org/binutils/docs/as/Skip.html
  - https://sourceware.org/binutils/docs/as/Short.html
  - https://sourceware.org/binutils/docs/as/Quad.html
  - https://sourceware.org/binutils/docs/as/String.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# GAS directives and sections
**Goal:** emit well-formed ELF objects from assembly.

```gas
        .text
        .globl  add3
        .type   add3, @function
add3:   lea     3(%rdi), %eax
        ret
        .size   add3, .-add3

        .section .rodata
        .p2align 3                      # align to 8, unambiguous on every target
tbl:    .quad   1, 2, 3
str:    .asciz  "text"                  # NUL-terminated

        .bss
        .lcomm  buf, 4096               # local zeroed space
        .comm   shared, 8, 8            # common symbol, optional alignment
```
- Visibility: `.global`/`.globl` makes a symbol visible to `ld`; `.local` (ELF) makes it not externally visible; `.hidden` sets ELF visibility to hidden so other components cannot see it; `.weak` marks weak symbols.
- `.size name, expression` sets a symbol's size, typically for functions, and the expression can use label arithmetic (`.-add3`).
- `.quad` emits 8-byte integers. `.byte` emits one byte per expression. `.short` is normally the same as `.word`, but the two can differ in length on some configurations, so check the target's machine-dependent notes. `.long` is the same as `.int`.
- `.asciz` is `.ascii` plus a zero byte for each string; `.string` also ends each string with a 0 byte. Strings not separated by commas in `.asciz` are concatenated with only one final zero byte.
- `.skip size[,fill]` emits size bytes of fill (default zero), same as `.space`. `.equ` is synonymous with `.set`.
- `.lcomm` reserves zeroed bss bytes for a symbol that is not global; `.comm` declares a common symbol that `ld` may merge with another definition, and on ELF it takes an optional third argument, the alignment in bytes (a power of two).

## Gotchas
- The meaning of `.align`'s argument varies by target: bytes on i386 ELF (`.align 8` is a multiple of 8) but the number of low-order zero bits on others (ppc, arm; `.align 3` is a multiple of 8). `.balign` and `.p2align` behave consistently across architectures, so prefer them.
- If the fill value of an alignment is omitted in a code section, the padding is normally no-op instructions on most systems.

## Self-check
Assemble, then run `readelf -S` and `nm -S` on the object and confirm sizes and sections match.

## Checked
Read the GNU as manual pages for .align, .comm, .lcomm, .local, .hidden, .size, .skip, .short, .quad, .string/.asciz, .global, .byte and .equ. Removed: the `%function` note for AArch64 and the `@` comment-character explanation, the `.note.GNU-stack` section and executable-stack gotcha, `.data` and `.rodata` section examples, `.zero` and `.value`, and the 2/4 byte sizes for `.word` per architecture (not stated on pages read).

Method: docs-checked 2026-11-09 against the GNU as manual directive pages listed in sources.
