---
id: computing-software.software-engineering.assembly.lldb-disassemble-step
name: lldb-disassemble-step
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, lldb-disassemble-step, asm-lldb]
level: practitioner
status: docs-checked
description: "Debug assembly in LLDB: stop at entry, disassemble by name, range or frame, single-step instructions with si and ni, and look up an address."
sources:
  - https://lldb.llvm.org/use/tutorial.html
  - https://lldb.llvm.org/use/map.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LLDB: disassemble and step
**Goal:** inspect and step machine code with LLDB.

```lldb
$ lldb ./prog
(lldb) process launch --stop-at-entry        # stop at the first instruction
(lldb) disassemble --name main               # by function
(lldb) disassemble --start-address 0x1eb8 --end-address 0x1ec3
(lldb) disassemble --start-address 0x1eb8 --count 20
(lldb) disassemble --frame                   # current function
(lldb) disassemble --frame --bytes           # include raw instruction bytes
(lldb) thread step-inst                      # one instruction (si)
(lldb) thread step-inst-over                 # step over calls (ni)
(lldb) image lookup --address 0x1ec4         # symbol for an address
```
- `si` and `ni` are the LLDB equivalents of GDB's `stepi` and `nexti`: `si` is `thread step-inst`, `ni` is `thread step-inst-over`.
- `disassemble --name main` is the LLDB form of GDB's `disassemble main`; `disassemble --start-address A --count N` replaces GDB's `x/Ni A`.
- To disassemble at every stop, add a stop hook: `target stop-hook add`, then type `bt` and `disassemble --pc` and finish with `DONE`.
- Remote debug with `gdb-remote`, which takes `host:port` or just a port, for example `gdb-remote 8000`.
- Options after `--` on `process launch` go to the program, so `process launch --stop-at-entry -- -program_arg value` passes `-program_arg value` to it.

## Gotchas
- Addresses in the examples are placeholders; take real ones from your own `disassemble` or `image lookup` output.

## Self-check
Disassemble `main`, step three instructions with `si`, and check where you are each time with `disassemble --pc`.

## Checked
2026-11-08. Checked against the LLDB tutorial page and the GDB to LLDB command map: `process launch --stop-at-entry` and the `--` separator, `disassemble` options (`--name`, `--frame`, `--start-address`, `--end-address`, `--count`, `--bytes`, `--pc`), `thread step-inst` and `thread step-inst-over` with `si` and `ni`, the stop-hook recipe, `image lookup --address`, `gdb-remote`. Removed (not stated on these pages): the `target.x86-disassembly-flavor` and `stop-disassembly-display` settings, `breakpoint set -a`, `register read pc`, the Mach-O and QEMU/gdbserver remarks, and the ASLR and load-address gotchas.

Method: documentation only; no commands were run.
