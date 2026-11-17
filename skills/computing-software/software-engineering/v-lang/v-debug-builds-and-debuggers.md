---
id: computing-software.software-engineering.v-lang.v-debug-builds-and-debuggers
name: v-debug-builds-and-debuggers
category: computing-software
field: software-engineering
product: v-lang
tags: [v-debug-builds-and-debuggers, errors-debugging-and-diagnostics, debugging, gdb, lldb, debugger, symbols, keepc, dump, v-lang]
level: practitioner
status: docs-checked
description: "Debug V binaries with -g or -cg, keep generated C with -keepc, view the C command with -showcc, debug with lldb or gdb, and trace values with dump()."
sources:
  - https://raw.githubusercontent.com/vlang/v/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debug builds with -g and using gdb or lldb

Goal: debug V programs at source level.

- `-g` produces a less optimised executable with more debug info. Generated C uses `#line` directives so debuggers and panic stack traces resolve positions to the original `.v` files. The docs say it is usually better to pass `-g`, unless you are writing low-level code, in which case use `-cg`.
- `-cg` also produces a less optimised executable with debug info, but uses C source line numbers. It is frequently combined with `-keepc` to inspect the generated C in a panic or in the debugger.
- `-keepc` keeps the generated C file after a successful compile at a stable path; `-showcc` prints the C compile command; `-show-c-output` prints the C compiler's output. For low-level C wrappers: `v -keepc -cg -showcc yourprogram.v`, then run gdb, lldb or an IDE on the executable.
- Command line: `v -g hello.v` then `lldb hello` (or gdb). The docs link to a V wiki page on debugging V executables in GDB, and to CodeLite and Visual Studio Code setup docs.
- Inspect generated C only: `-o file.c` produces `file.c` and stops; `-printfn main -o file.c` shows the C for a single function.
- Tests: `v -g -keepc prog_test.v`; `-keepc` is needed so the executable is not deleted after the run.
- On macOS, debug builds keep a `.dSYM` bundle beside the executable.
- `v help`, `v help build` and `v help build-c` list all flags.
- Quick tracing: `dump(expr)` traces the value of any expression together with its source location and returns the value; `eprintln` writes to stderr.

Verify: hit a breakpoint in a V function and print a local.

## Checked
2026-11-08. Checked against the Debugging section and the `dump` section of the V documentation (`doc/docs.md`). Removed (not stated there): gdb/lldb command sequences and the `main__main` name-mangling scheme, the VS Code CodeLLDB recipe, the `dbg` module and `dbg.breakpoint()`, the claim that tcc debug info is weaker, and `$if debug` with `-d debug` (the docs tie `$if debug` to `-g`/`-cg`). Replaced landing-page sources with the raw docs file.
Method: documentation only; no commands were run.
