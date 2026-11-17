---
id: computing-software.software-engineering.assembly.nasm-data-directives
name: nasm-data-directives
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, nasm-data-directives, asm-nasm]
level: practitioner
status: docs-checked
description: "NASM data definition and constants: DB/DW/DD/DQ, TIMES, RESB, EQU versus %define and %assign, STRUC, INCBIN and alignment."
sources:
  - https://www.nasm.us/doc/nasm03.html
  - https://www.nasm.us/doc/nasm05.html
  - https://www.nasm.us/doc/nasm06.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# NASM data directives and constants
**Goal:** define initialised and uninitialised data cleanly.

```nasm
section .data
bytes:  db 1, 2, 3, "text", 0
words:  dw 0x1234
ints:   dd 100, -5
big:    dq 0x1122334455667788
pi:     dq 3.14159          ; double
pad:    times 16 db 0
        align 16
section .bss
buf:    resb 4096
count:  resq 1
section .text
BUFSZ   equ 4096
len     equ $ - bytes        ; assembly-time constant
%define SHIFT 3
%assign n 1                  ; numeric, redefinable
struc Point
    .x: resd 1
    .y: resd 1
endstruc                      ; defines Point_size
blob:   incbin "data.bin"
```
- `db dw dd dq dt` (also `do dy dz`) declare initialised data; floating-point constants are accepted by `db dw dd dq dt do`, and a decimal point is mandatory so `dd 1` is an integer and `dd 1.0` a float. `dq` takes a double-precision float, `dt` an extended-precision one, `dw` an IEEE half-precision one. `dt do dy dz` do not accept integer operands.
- `resb resw resd resq rest reso resy resz` reserve uninitialised space and are meant for the BSS section. Since NASM 2.15 the MASM-style `?` and `DUP` also work (`db 64 dup (?)`).
- `times` assembles its operand repeatedly. Its count is a critical expression (it may only use symbols already defined), and it cannot repeat a macro: use `%rep` for that.
- `equ` defines an absolute constant that cannot be redefined; its value is computed once, with `$` taken at the line where it appears. `%define` is single-line macro text substitution, and `%assign` defines a numeric macro evaluated once when processed, which may be redefined (`%assign i i+1`).
- `struc Name` ... `endstruc` is a preprocessor macro pair: `Name_size` is defined as an `equ` giving the structure size, and fields declared with `resb`-family instructions become offsets. Local-label style names give `Point.x`; use them as constants in addressing such as `[rdi + Point.x]`. NASM has no period notation on instances: `[mystruc.mt_word]` is invalid, write `[mystruc + mt_word]`.
- `align 16` (and `alignb` for BSS) is a macro that pads with `nop` by default; it works relative to the start of the section, and does not check that its argument is a power of two.
- `incbin "file", skip, max` includes a file verbatim, optionally skipping bytes and limiting the count.

## Gotchas
- Because `len equ $ - bytes` evaluates `$` where the `equ` line sits, put it directly after the data it measures with nothing in between.
- Aligning to 16 in a section that is only guaranteed 4-byte alignment is wasted effort; `align` does not check this.
- `$` inside a `dx` statement is only defined for the first expression or for `value - $`.

## Self-check
Print `Point_size` and use `Point.y` to read the second field of an array element.

## Checked
2026-11-08. Checked against the NASM 3.02 manual: chapter 3 (pseudo-instructions Dx, RESx, INCBIN, EQU, TIMES, floating-point constants, critical expressions), chapter 5 (%define, %assign) and chapter 6 (STRUC/ENDSTRUC and the `_size` symbol, ALIGN/ALIGNB). Removed: the byte-size list for db/dw/dd/dq/dt and the claim that the loader zeroes `.bss` (neither stated in the pages read).

Method: documentation only; no commands were run.
