---
id: computing-software.software-engineering.assembly.alignment-padding
name: alignment-padding
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, alignment-padding, asm-performance]
level: advanced
status: docs-checked
description: "Alignment directives: GAS .align/.balign/.p2align semantics and fill rules, NASM ALIGN/ALIGNB and the smartalign package with ALIGNMODE."
sources:
  - https://sourceware.org/binutils/docs/as/Align.html
  - https://sourceware.org/binutils/docs/as/Balign.html
  - https://sourceware.org/binutils/docs/as/P2align.html
  - https://sourceware.org/binutils/docs/as/i386_002dOptions.html
  - https://www.nasm.us/doc/nasm06.html
  - https://www.nasm.us/doc/nasm07.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Alignment and code layout
**Goal:** align code and data with the right directive and padding.

```nasm
%use smartalign
alignmode p6                ; NASM: pad code alignment with long NOPs (Intel)
align 16
hot_loop:
```
```gas
        .p2align 4          # 2^4 = 16: low 4 bits of the location counter are zero
hot_loop:
        .balign 16          # same, but the argument is a byte count
```
- GAS `.balign N` takes the alignment in bytes and `.p2align N` the number of low-order zero bits (`.p2align 3` = multiple of 8). Both behave the same on every architecture. Plain `.align` varies by target: bytes on i386/ELF and several others, power of two on others (ppc, arm, i386 a.out), so prefer `.balign` or `.p2align` in portable code.
- Optional second argument is the fill value; third is the maximum number of bytes to skip (if more would be needed, no alignment is done). If the fill is omitted, padding is normally zero, except that on most systems a code section is filled with no-op instructions. `.balign 16,,8` skips the fill but keeps the limit.
- `.balignw`/`.balignl` (and the `.p2align` equivalents) treat the fill pattern as a 2-byte or 4-byte value.
- NASM `align N` and `alignb N` need a power of two. `align` pads with `NOP` by default, `alignb` reserves bytes (`resb 1`) for BSS; a second argument (`align 8,db 0`) replaces the filler and must generate exactly one byte (no error checking is done).
- NASM alignment is relative to the start of the section, so aligning to 16 in a section only aligned to 4 does nothing useful. `align` also calls `SECTALIGN` implicitly.
- With `%use smartalign`, `align` without a second argument emits instructions more efficient than a run of `NOP`s, and jumps over the padding when it exceeds a threshold. `ALIGNMODE` takes a mode (`generic` default, `nop`, `k7`, `k8`, `p6`) and an optional jump threshold; `-1` or `nojmp` disables the jump. `p6` uses long NOPs from the Pentium Pro and is incompatible with CPUs of family 5 or lower.
- GAS on x86 has `-mbranches-within-32B-boundaries`, which aligns conditional jumps, fused conditional jumps and unconditional jumps within a 32-byte boundary using up to 5 segment prefixes on an instruction. It is equivalent to `-malign-branch-boundary=32 -malign-branch=jcc+fused+jmp -malign-branch-prefix-size=5`.

## Gotchas
- Plain GAS `.align 3` means 8 bytes on some targets and 3 bytes' worth of zero bits on others.
- NASM `align` with a multi-byte second argument silently does the wrong thing.

## Self-check
Assemble `.p2align 4` between two labels and confirm with `objdump -d` that the second label address is a multiple of 16.

## Checked
Method: docs-checked 2026-11-09 against the GNU as pages Align, Balign and P2align, the as x86 options page (-mbranches-within-32B-boundaries), and NASM manual chapter 6 (section 6.15, ALIGN/ALIGNB/SECTALIGN) and chapter 7 (smartalign). Dropped unconfirmed claims about fetch and cache benefits, cache-line and SIMD alignment sizes, AArch64 alignment and the Intel JCC erratum and binutils version.
