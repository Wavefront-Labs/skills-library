---
id: computing-software.software-engineering.assembly.gdb-registers-memory
name: gdb-registers-memory
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, gdb-registers-memory, asm-gdb]
level: practitioner
status: draft
description: "Inspect registers and memory in GDB: info registers, print formats, flags, vector registers, x command formats and sizes, watchpoints and writing state."
sources:
  - https://sourceware.org/gdb/documentation/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# GDB: registers and memory
**Goal:** read and modify machine state precisely.

```gdb
(gdb) info registers                    # general registers
(gdb) info registers rip rsp eflags
(gdb) p/x $rax                          # hex
(gdb) p $eflags                         # shows set flags, e.g. [ ZF PF ]
(gdb) p $xmm0                           # union of lane views
(gdb) p $xmm0.v4_float
(gdb) info all-registers                # includes vector and system registers
(gdb) x/16xb $rsp                       # 16 bytes in hex
(gdb) x/4gx $rsp                        # 4 giant (8-byte) words, hex
(gdb) x/s 0x402000                      # C string
(gdb) x/3i $pc                          # 3 instructions
(gdb) set $rax = 5
(gdb) set {int}0x404028 = 1             # write memory
(gdb) watch *(long *)0x404028           # hardware watchpoint
(gdb) p $x0 ; p $sp ; p $cpsr           # AArch64 names
```
- `x/NFU address`: count N, format F (`x d u o t a c f s i`), unit U (`b h w g`).
- `p/t` prints binary, `p/c` characters, `p/d` signed decimal.
- Use `$pc`, `$sp`, `$fp` as architecture-neutral aliases.
- Record a session with `record full` for reverse stepping on supported targets.

## Gotchas
- `x` after `x` continues from the last address; reset by giving an address.
- Watchpoints on stack locals stop being meaningful after the frame returns.

## Self-check
Single-step `push rax` and verify memory at the new `rsp` with `x/gx`.
