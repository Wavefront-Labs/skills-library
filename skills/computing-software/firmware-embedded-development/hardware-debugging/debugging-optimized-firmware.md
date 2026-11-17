---
id: computing-software.firmware-embedded-development.hardware-debugging.debugging-optimized-firmware
name: debugging-optimized-firmware
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [optimized-code-debugging, optimized-out, og, inlining, disassembly, debug-info, gdb, hardware-debugging, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Debug -O2/-Os firmware: -Og and -g3, -fno-inline, DWARF level, stepping by instruction, and how GDB shows inlined functions and finish values."
sources:
  - https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html
  - https://gcc.gnu.org/onlinedocs/gcc/Debugging-Options.html
  - https://sourceware.org/gdb/current/onlinedocs/gdb.html/Inline-Functions.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging optimised code

Release firmware often only fits or meets timing at `-Os`/`-O2`, and some bugs only appear there.

## Build for debuggability without losing the bug
- `-g` requests debug info; `-g3` (level 3) adds extra information such as all macro definitions, which some
  debuggers can expand.
- GCC recommends `-Og` with `-g` when you are not using another optimisation option: it is meant for the standard
  edit-compile-debug cycle. It enables the `-O1` flags except those known to greatly interfere with debugging, and
  enables `-fvar-tracking-assignments` and `-fvar-tracking` so debug info in prologue and epilogue is better than
  at `-O0`.
- `-fvar-tracking-assignments` annotates assignments to user variables so debug info survives optimisation; GCC
  recommends `-gdwarf-4` along with it. Match the DWARF version to what your GDB supports.
- `-fno-inline` stops inline expansion except for functions marked `always_inline`; it is the default when not
  optimising. A single function can be exempted with the `noinline` attribute. The bug may move when you change
  optimisation, so confirm it still reproduces.
- `-fno-omit-frame-pointer` keeps frame pointers, but the manual notes it does not guarantee that they are used in
  all functions (several targets always omit them in leaf functions).
- When linking with link-time optimisation, debug info needs `-g` at compile time, and elaborate settings such as
  `-gdwarf-5` must be repeated on the link command line.

## Reading the session
- `<optimized out>` means a variable has no location at the current PC. Step to where it is used or look at
  registers and the disassembly instead.
- When source lines jump around, step by instruction with `stepi` / `nexti`; the GDB manual says single-instruction
  steps always show the inlined body.
- Inlined functions: GDB shows them in backtraces, lets you see their arguments and locals, step into them with
  `step`, skip with `next`, and leave with `finish`. `info frame` tells you whether a function was inlined. GDB needs
  the compiler's inlining debug info (it documents DWARF 2 support, with GCC 4.1 or later).
- A breakpoint at the call site of an inlined function may not work (the call site holds no code and GDB may move it
  to the next line). Set it on an earlier line or inside the inlined function.
- After `finish`, GDB cannot locate the return value of an inlined call; step to the next line and print the variable
  where the program stored it.

## Bugs that only appear optimised
- `-fstrict-aliasing` is enabled at `-O2`, `-O3` and `-Os`, so code that reads memory through an incompatible pointer
  type can change behaviour when optimised. The manual allows type-punning through a union in C.
- Compare disassembly at the optimisation level you ship, not only the source, and explain the root cause at the
  instruction level.

## Verify
- [ ] The debug build uses the same optimisation as release for the module under test.
- [ ] Root cause explained at the instruction level, not "it works at -O0".

## Checked
Method: docs-checked 2026-11-09 against GCC manual pages Optimize Options (read in part: -Og, -fno-inline, -fno-omit-frame-pointer, -fstrict-aliasing, LTO debug notes) and Debugging Options (read in part: -g levels, -fvar-tracking-assignments, -gdwarf), and the GDB manual page Inline Functions (read in full). Removed unconfirmed claims: OpenMP-style per-function optimize attribute and CMake recipe, volatile and delay-loop advice, UBSan, memory barriers, tail-call and r0 return notes, DWARF 5 garbage on old GDB.
