---
id: computing-software.software-engineering.c.gdb-watchpoints-and-conditional-breakpoints
name: gdb-watchpoints-and-conditional-breakpoints
category: computing-software
field: software-engineering
product: c
tags: [c, watchpoint, conditional-breakpoint, gdb-commands, reverse-debugging, tbreak]
level: advanced
status: docs-checked
description: "Use gdb watchpoints, conditional breakpoints and command lists to find who corrupts a variable."
sources: ["https://en.cppreference.com/w/c", "https://www.open-std.org/jtc1/sc22/wg14/", "https://sourceware.org/gdb/documentation/", "https://valgrind.org/docs/manual/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gdb watchpoints and conditional breakpoints

Goal: catch the exact write that breaks an invariant.

- Hardware watchpoint: `watch var` (or `watch -l *ptr` to watch the address). `rwatch` breaks on reads, `awatch` on both. `info watchpoints` lists them; hardware support depends on the target; software watchpoints single-step and are hundreds of times slower than normal execution, and `rwatch`/`awatch` can only be hardware.
- Conditional: `break file.c:120 if i == 99`; `condition N expr` edits; `ignore N count` skips hits; `tbreak` is one-shot.
- Scripted: `commands N` ... `silent` ... `print x` ... `continue` ... `end` for logging without stopping.
- `finish` runs to caller and shows the return value; `until`/`advance` skip loops; `display expr` prints at every stop.
- Reverse execution: `record` then `reverse-continue`, `reverse-step` (see Reverse Execution).
- Attach to a running process: `gdb -p PID`; may need `ptrace_scope` change (`/proc/sys/kernel/yama/ptrace_scope`).

Verify: watch a counter in a test loop and confirm gdb stops on the statement that modified it.

## Checked

2026-11-02. Confirmed in the GDB manual (Set Watchpoints, Set Breaks, Conditions, Break Commands, Reverse Execution, Auto Display, Attach) and ptrace(2): `watch/rwatch/awatch -l`, `info watchpoints`, `ignore bnum count`, `tbreak`, `commands`/`silent`, `reverse-continue`, `display`, `/proc/sys/kernel/yama/ptrace_scope`. Removed: the x86 four-slot figure, the `watch *(int *)` form and the `rr` remark.

Method: documentation only; no commands were run.
