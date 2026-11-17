---
id: computing-software.software-engineering.d.d-debugging-profiling-sanitizers
name: d-debugging-profiling-sanitizers
category: computing-software
field: software-engineering
product: d
tags: [d-debugging-profiling-sanitizers, dev-tools, debugging, gdb, lldb, valgrind, perf, profile, sanitizer, asan, stacktrace, vsdebug, profile-gc, symbol-demangling, d]
level: practitioner
status: docs-checked
description: "Debug D programs with -g and gdb/lldb/VS debugger (D demangling), profile with -profile, perf, valgrind, ldc -fsanitize, and diagnose GC and stack overflows."
sources:
  - https://dlang.org/dmd-linux.html
  - https://wiki.dlang.org/Debugging
  - https://dlang.org/phobos/core_exception.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging and profiling: gdb, -g, -profile, -vgc

Goal: find crashes and hot spots.

- Build with symbols: `dmd -g -debug app.d`. `-g` adds DWARF debug info for debuggers such as gdb; `-gf` emits debug info for all referenced types; `-debug` compiles `debug` code.
- Debugger support (D wiki): on Linux DWARF with GDB is listed as good support (breakpoints, stack frames, variable inspection); on Windows OMF with Mago/VisualD and Visual Studio; VS Code with the C/C++ extension or Native Debug can drive GDB/LLDB.
- Profiling: `dmd -profile app.d`, run the program, and read `trace.log` (fan in/out and timing per function) and `trace.def` (linker ordering hints). `-profile=gc` writes `profilegc.log` at exit with instrumented GC allocations (language constructs, Phobos allocations, `core.memory.GC` calls).
- `-vgc` lists all GC allocations, including hidden ones, at compile time.
- Bounds checking: `-boundscheck=[on|safeonly|off]`; `on` is the default, `safeonly` is the default for `-release`. A failed check raises `core.exception.RangeError`.

Gotchas:
- `-O -inline` can merge frames and make traces harder to read.
- `-profile` instruments the code; do not use its timings as absolute numbers.

Verify: reproduce a bug under gdb on a `-g` build and print the faulting slice's `length`.

## Checked

2026-11-03. Confirmed against: the DMD command-line page (`-g`, `-gf`, `-debug`, `-profile`, `-profile=gc`, `-vgc`, `-boundscheck`, `-O`, `-inline`, `trace.log`, `trace.def`, `profilegc.log`), the D wiki Debugging page and core.exception.

Removed because the pages read did not confirm it: gdb `set print asm-demangle` and `ddemangle`/`c++filt`/pretty-printer package claims, `-L--export-dynamic` backtrace advice, `TraceInfo`, perf/valgrind/callgrind/massif recipes, LDC `-fprofile-instr-generate` and `-fsanitize=address`, `ulimit -s` stack advice, `ldc2 -g -O0`.

Method: documentation only; no commands were run.
