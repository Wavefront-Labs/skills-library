---
id: computing-software.software-engineering.assembly.gdb-stepi-disassemble
name: gdb-stepi-disassemble
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, gdb-stepi-disassemble, asm-gdb]
level: practitioner
status: draft
description: "Debug assembly with GDB: starti, stepi/nexti, disassemble in Intel flavour, x/i, display/i, breakpoints on addresses and the TUI asm layout."
sources:
  - https://sourceware.org/gdb/documentation/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# GDB: disassemble and single-step
**Goal:** trace execution instruction by instruction.

```gdb
$ gdb ./prog
(gdb) set disassembly-flavor intel      # x86 only; put in ~/.gdbinit
(gdb) starti                            # stop at the very first instruction
(gdb) break _start                      # or break *0x401000
(gdb) run
(gdb) disassemble                       # current function
(gdb) disassemble /r _start             # with raw bytes
(gdb) x/8i $pc                          # next eight instructions
(gdb) display/i $pc                     # show next instruction after every stop
(gdb) stepi                             # one instruction (si); enters calls
(gdb) nexti                             # one instruction, steps over calls (ni)
(gdb) stepi 5
(gdb) info line *$pc
(gdb) layout asm                        # TUI assembly window
```
- `starti` works even when there is no `main` or symbols; `break` on an address needs the `*` prefix.
- Use `tbreak` for one-shot breakpoints and `until`/`advance` to run to a location.
- Use `set disassemble-next-line on` to print the next instruction at every stop.
- Cross-debug an AArch64 program with `gdb-multiarch` plus `qemu-aarch64 -g 1234 ./prog` and `target remote :1234`.

## Gotchas
- `step`/`next` need line info; for assembly without `-g`, use `stepi`/`nexti`.
- `disassemble` without a symbol at the pc fails; give a range `disassemble 0x401000,0x401040`.

## Self-check
Single-step a call and watch `rsp` and the return address before and after `ret`.
