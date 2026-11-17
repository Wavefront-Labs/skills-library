---
id: computing-software.firmware-embedded-development.hardware-debugging.gdb-python-scripting
name: gdb-python-scripting
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [gdb-python-scripting, gdb, python-api, pretty-printers, custom-commands, breakpoint-stop-hook, arm-none-eabi-gdb, debug-automation, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Extend GDB with Python for firmware debugging: custom commands, pretty printers for RTOS/driver structs, logging breakpoints that do not halt, and memory and register reads."
sources:
  - https://sourceware.org/gdb/current/onlinedocs/gdb.html/Python-API.html
  - https://sourceware.org/gdb/current/onlinedocs/gdb.html/CLI-Commands-In-Python.html
  - https://sourceware.org/gdb/current/onlinedocs/gdb.html/Breakpoints-In-Python.html
  - https://sourceware.org/gdb/current/onlinedocs/gdb.html/Writing-a-Pretty_002dPrinter.html
  - https://sourceware.org/gdb/current/onlinedocs/gdb.html/Inferiors-In-Python.html
  - https://sourceware.org/gdb/current/onlinedocs/gdb.html/Auto_002dloading-safe-path.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GDB Python scripting

**Goal:** turn repetitive inspection (walk a linked list of tasks, decode a register, log every
call to a function) into one command, on any GDB connected to OpenOCD, J-Link or pyOCD.

## Setup
- Your GDB (for example `arm-none-eabi-gdb`) must be built with Python support. `python help (gdb)`
  at the GDB prompt gives online help for the API.
- Load scripts with `source tools/gdb/fw.py`, or from a `.gdbinit`. GDB only auto-loads files
  from directories trusted by the `set auto-load safe-path` setting.

## Custom command
Subclass `gdb.Command`, register it from `__init__` (name, command class such as
`gdb.COMMAND_USER`) and implement `invoke(self, arg, from_tty)`.
```python
import gdb
class Tasks(gdb.Command):
    """tasks: list tasks from the scheduler's linked list"""
    def __init__(self): super().__init__("tasks", gdb.COMMAND_USER)
    def invoke(self, arg, from_tty):
        node = gdb.parse_and_eval("g_task_list")
        while int(node) != 0:
            t = node.dereference()
            print(f"{t['name'].string():16} prio={int(t['prio'])} sp=0x{int(t['sp']):08x}")
            node = t['next']
Tasks()
```

## Logging breakpoint (does not stop)
Subclass `gdb.Breakpoint` and define `stop`. If it returns True the inferior stops, otherwise
it continues.
```python
class LogCall(gdb.Breakpoint):
    def stop(self):
        v = gdb.parse_and_eval("len")
        print(f"spi_xfer len={int(v)}")
        return False            # continue running
LogCall("spi_xfer")
```
Each hit still halts the core briefly to run your Python, so timing changes; for the simple case
use `dprintf`, and RTT or trace for timing-sensitive code. If several breakpoints at one location
define `stop`, all are called, and one returning True is enough to stop.

## Pretty printer
```python
import gdb.printing
class FixedQ16Printer:
    def __init__(self, val): self.val = val
    def to_string(self): return f"{int(self.val['raw']) / 65536:.5f}"
pp = gdb.printing.RegexpCollectionPrettyPrinter("fw")
pp.add_printer("q16", "^q16_t$", FixedQ16Printer)
gdb.printing.register_pretty_printer(gdb.current_objfile(), pp)
```

## Raw memory, registers and commands
```python
inf = gdb.selected_inferior()
cfsr = int.from_bytes(inf.read_memory(0xE000ED28, 4), "little")
pc = int(gdb.selected_frame().read_register("pc"))
out = gdb.execute("info registers", to_string=True)   # capture command output
```
`Inferior.read_memory(address, length)` returns a buffer object. `gdb.execute(cmd, to_string=True)`
returns the output as a string instead of printing it.

## Gotchas
- Arithmetic on `gdb.Value` objects returns `gdb.Value` objects; convert with `int()` before
  Python maths.
- A `gdb.Value` has `is_optimized_out`; check it before using variables from optimised code.
- GDB errors raised by commands run from Python become `gdb.error` exceptions; reading invalid
  inferior memory raises a subclass of it (`gdb.MemoryError`). Catch them in scripts that may
  run without a live target.
- Check `gdb.selected_inferior().pid` (an Inferior attribute) before assuming a running process.

## Verify
- [ ] `tasks` output matches the RTOS-aware view of the IDE.
- [ ] The logging breakpoint prints without the user having to `continue`.

## Checked
Confirmed: gdb.Command and COMMAND_USER and invoke (CLI Commands In Python), Breakpoint.stop
semantics (Breakpoints In Python), RegexpCollectionPrettyPrinter, register_pretty_printer and
current_objfile (Writing a Pretty-Printer), read_memory, selected_inferior and pid (Inferiors In
Python), read_register (Frames In Python), gdb.execute to_string (Basic Python), is_optimized_out
(Values From Inferior), gdb.error (Exception Handling), and `set auto-load safe-path` (Auto-loading safe path). Removed as
unconfirmed: the Arm toolchain 12+ and Python-version statement (the Arm download page was not
readable), `-rtos auto`, gdb-dashboard, PyCortexMDebug references and `monitor reset halt`.

Method: docs-checked 2026-11-09 against the GDB manual pages Python API, CLI Commands In Python, Breakpoints In Python, Writing a Pretty-Printer, Inferiors In Python, Basic Python, Values From Inferior and Exception Handling.
