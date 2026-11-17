---
id: computing-software.software-engineering.assembly.objdump-disassemble
name: objdump-disassemble
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, objdump-disassemble, asm-binutils]
level: intro
status: docs-checked
description: "Disassemble binaries with GNU objdump: Intel syntax, symbol ranges, relocations, source interleaving, section dumps and the -b/-m overrides."
sources:
  - https://sourceware.org/binutils/docs/binutils/objdump.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# objdump disassembly
**Goal:** read machine code in executables and objects.

```sh
objdump -d prog                          # disassemble code sections
objdump -d -M intel prog                 # Intel syntax (x86 -M intel / att)
objdump -d -M intel --no-show-raw-insn prog     # hide opcode bytes
objdump -dr foo.o                        # relocations interspersed with disassembly
objdump -d -S -l foo.o                   # source plus file:line (needs debug info)
objdump -d -j .text --start-address=0x401000 --stop-address=0x401040 prog
objdump -d --disassemble=main prog       # one symbol
objdump -t prog                          # symbol table
objdump -s -j .rodata prog               # hex dump of a section
```
- `-d` (`--disassemble`) disassembles only the sections expected to contain instructions; `-D` disassembles the contents of all non-empty non-bss sections, and `-j name` selects specific sections.
- `-d` assumes symbols in a code section fall on instruction boundaries and will not disassemble across one; `-D` drops that assumption, so `-d` and `-D` output can differ when data sits in code sections.
- `--disassemble=symbol` starts at the symbol; for a function it stops at the function end, otherwise at the next symbol. If nothing matches, nothing is shown.
- `-r` prints relocation entries; with `-d`/`-D` they appear interspersed with the disassembly.
- `-S` mixes source with disassembly where possible and implies `-d`; `-l` labels output with file name and line numbers from debug information (useful with `-d`, `-D` or `-r`).
- `-C` demangles symbol names.
- `-M options` passes target-specific options to the disassembler and may be repeated or comma-separated. On x86 the options include `intel`/`att` (syntax), `x86-64`/`i386`/`i8086`, and `amd64`/`intel64`.
- `-b bfdname` sets the object format and `-m machine` the architecture when the file does not describe them; `-i` lists the available formats and architectures.
- `--start-address` and `--stop-address` limit what `-d`, `-r` and `-s` show.
- `-s` (`--full-contents`) dumps section contents, by default all non-empty non-bss sections, so combine it with `-j`.
- `--show-raw-insn` prints instruction bytes as well; it is the default except with `--prefix-addresses`.

## Gotchas
- A disassembly starting mid-instruction on x86 shows plausible nonsense; start at a symbol or known boundary.
- `-D` on data sections prints the bytes as if they were instructions.

## Self-check
Disassemble your own `add2` object with and without `-r` and explain the differences.

## Checked
2026-11-08. Checked against the binutils objdump manual page (options -b, -m, -M, -C, -d, -D, -j, -l, -r, -s, -S, -t, -i, --disassemble=symbol, --start-address, --stop-address, --show-raw-insn). Removed: the claim that AT&T is the default x86 syntax, the raw-binary examples (`-b binary`), the AArch64 and cross-prefixed objdump examples, the llvm-objdump claim, the linker padding claim and the call-target placeholder claim, none of which the page states.

Method: documentation only; no commands were run.
