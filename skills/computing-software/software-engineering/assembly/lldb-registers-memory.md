---
id: computing-software.software-engineering.assembly.lldb-registers-memory
name: lldb-registers-memory
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, lldb-registers-memory, asm-lldb]
level: practitioner
status: docs-checked
description: "Inspect state in LLDB: register read and write, memory read with format, size and count, frame variable and memory watchpoints."
sources:
  - https://lldb.llvm.org/use/tutorial.html
  - https://lldb.llvm.org/use/map.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LLDB: registers and memory
**Goal:** examine and change registers and memory.

```lldb
(lldb) register read                       # general purpose registers
(lldb) register read rax rsp rbp           # named registers
(lldb) register read --all                 # all register sets
(lldb) register read --format binary rax   # or: register read/t rax
(lldb) register write rax 123
(lldb) register write pc `$pc+8`           # backticks insert an expression result
(lldb) memory read --size 4 --format x --count 4 0xbffff3c0
(lldb) x/4xw 0xbffff3c0                    # GDB-style form, same read
(lldb) memory read --gdb-format 4xw 0xbffff3c0
(lldb) watchpoint set expression -- my_ptr
(lldb) watchpoint list
```
- LLDB tries to use printf-style format characters; type `help format` for the full list.
- `watchpoint set expression` takes raw input, evaluated as an expression giving the start of the region after the `--` terminator. The region size defaults to the pointer size unless you pass `-x byte_size`.
- Any command can inline a scalar expression result (while the target is stopped) by wrapping the expression in backticks.
- `frame variable` shows source variables when debug info is present; use registers for assembly-only code.
- Memory read and write can be used while the process runs (`memory [read|write] ...`).

## Gotchas
- Check addresses against your own process; the ones above are placeholders.

## Self-check
Read four words at `$sp` in both `memory read` and `x/4xw` forms and confirm they match.

## Checked
2026-11-08. Checked against the LLDB tutorial page and the GDB to LLDB command map: `register read` (plain, named, `--all`, `--format`, `/t`, `/d`), `register write` including the backtick expression, `memory read` with `--size --format --count`, the `x/4xw` and `--gdb-format` forms, `watchpoint set expression` and its size default, `frame variable`, memory read/write while running. Removed (not on these pages): the `memory write ADDR VALUE` syntax, `expression -f x`, `p/x $rax`, `register read x0 x1 sp pc`, the format-letter list, vector-lane format strings, the GDB `x` shorthand caveat and the four-hardware-watchpoint limit.

Method: documentation only; no commands were run.
