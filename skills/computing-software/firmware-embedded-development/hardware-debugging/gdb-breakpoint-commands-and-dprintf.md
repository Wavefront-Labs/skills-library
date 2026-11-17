---
id: computing-software.firmware-embedded-development.hardware-debugging.gdb-breakpoint-commands-and-dprintf
name: gdb-breakpoint-commands-and-dprintf
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [dprintf, breakpoint-commands, conditional-breakpoint, ignore-count, gdb, hardware-debugging, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Instrument firmware from GDB without rebuilding: dprintf and its styles, breakpoint command lists that print and continue, conditions, ignore counts."
sources:
  - https://sourceware.org/gdb/current/onlinedocs/gdb.html/Dynamic-Printf.html
  - https://sourceware.org/gdb/current/onlinedocs/gdb.html/Break-Commands.html
  - https://sourceware.org/gdb/current/onlinedocs/gdb.html/Conditions.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Breakpoint commands and dprintf

## dprintf: printf without a rebuild
```gdb
dprintf uart.c:142,"rx len=%u state=%d\n", len, s->state
dprintf i2c_xfer,"addr=0x%02x\n", addr
info breakpoints          # dprintfs are listed as breakpoints with their printf and continue commands
```
`dprintf locspec,template,expression[,expression...]` combines a breakpoint with formatted printing. `set dprintf-style`
chooses how the output is handled, and a change affects all existing dprintfs immediately:
- `gdb` (the default) uses GDB's own `printf`.
- `call` calls a function in the target program, normally `printf` (`set dprintf-function`, `set dprintf-channel`
  for `fprintf`-style channels). Only format specifiers the target function supports are safe.
- `agent` lets the remote agent (for example gdbserver) print; only for agents that can run commands on the target.

## Command lists
```gdb
break spi_transfer
commands
  silent
  printf "tx=%p n=%d\n", tx, n
  continue
end
```
- `silent` must be the first line of the list; it suppresses the usual stop message.
- Commands after one that resumes execution (`continue`, `step`, `next`) are ignored.
- Inside a list, `disable $_hit_bpnum` disables the breakpoint that was hit.
- A list can also change state to compensate for another bug, for example `set x = y + 4` followed by `cont`
  (the manual's example), so you can test for a second bug.
- With no argument, `commands` applies to the last breakpoint set, not the one most recently hit.

## Conditions and counts
```gdb
break adc_isr if sample > 4000
condition 3 g_errors != 0
condition 3                # remove the condition
ignore 3 999               # skip the next 999 hits; it stops on the 1000th
```
- `condition` checks the expression's syntax and symbols immediately, but does not evaluate it.
- With a positive ignore count and a condition, the condition is not checked until the count reaches zero.
- By default GDB evaluates conditions itself. If the target supports it, conditions can be evaluated on the target
  (as agent expressions) so GDB is only told when the condition is true.
- Conditions can have side effects and call target functions, but breakpoint command lists are usually more flexible.
  If another enabled breakpoint sits at the same address, GDB may see it first and stop without checking the condition.

## Costs
Every dprintf or command-list hit is a breakpoint stop: the target is halted, GDB acts, then resumes. A hot ISR with a
dprintf changes its timing, so timing-dependent bugs can disappear or new ones appear. Use RTT/ITM logging for hot
paths. Check the probe's and core's hardware breakpoint limits in their own documentation.

## Verify
- [ ] Output appears while the program keeps running (check loop timing with a GPIO toggle).
- [ ] `info breakpoints` shows the expected dprintf, condition and ignore counts.

## Checked
Method: docs-checked 2026-11-09 against the GDB manual pages Dynamic Printf, Breakpoint Command Lists and Break Conditions (all read in full). Removed unconfirmed claims: OpenOCD not supporting agent style, tbreak/hbreak notes, Cortex-M comparator counts, per-hit millisecond cost, DBGMCU freeze register, save breakpoints.
