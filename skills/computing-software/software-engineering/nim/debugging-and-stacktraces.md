---
id: computing-software.software-engineering.nim.debugging-and-stacktraces
name: debugging-and-stacktraces
category: computing-software
field: software-engineering
product: nim
tags: [debugging-and-stacktraces, compiler-commands-and-backends, debugging, gdb, lldb, stacktrace, debugger-native, stacktrace-on, linetrace, logging, dump, nim]
level: practitioner
status: docs-checked
description: "Enable stack traces and line info, debug with gdb/lldb, use --debugger:native, and trace with echo, dump and logging."
sources:
  - https://nim-lang.org/docs/nimc.html
  - https://nim-lang.org/docs/intern.html
  - https://nim-lang.org/docs/assertions.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging: stack traces, debugger and logging

Goal: find bugs in Nim programs.

- `--stackTrace:on|off` and `--lineTrace:on|off` control tracing (`--lineTrace` implies `--stackTrace`); when `--stackTrace` is on the generated C contains stack-trace code.
- Native debugging: `--debugger:native` enables `--debuginfo --lineDir:on` for use with GDB, LLDB or CDB.
- Inspect values with `repr`, `dump(x)` (std/sugar) or `debugEcho`.
- `std/logging`: `addHandler(newConsoleLogger())`, then `info(...)`, `error(...)`.
- Assertions: `doAssert cond, "msg"` is always on, regardless of `--assertions` or `-d:danger`; `assert` follows `--assertions`.
- `--panics:on|off` turns panics into process terminations (default off).
- Print a trace anywhere: `writeStackTrace()`.

Verify: the native debugger stops at your breakpoint on a Nim source line.

## Checked

2026-11-02. Confirmed against basicopt.txt (`--lineTrace`, `--debugger:native`), nimc.md (stack trace section), intern.md (`--debugger:native`, `writeStackTrace`), lib/std/assertions.nim (`doAssert`), lib/pure/logging.nim and sugar.nim, lib/system.nim (`writeStackTrace`, `debugEcho`). Removed: gdb breakpoint syntax, `x_123` name mangling, `-d:debug`, ASan and `--sanitize`, the optimiser and obsolete-`--debugger:on` gotchas.
Method: documentation only; no commands were run.
