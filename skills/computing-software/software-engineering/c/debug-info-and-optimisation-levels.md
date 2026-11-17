---
id: computing-software.software-engineering.c.debug-info-and-optimisation-levels
name: debug-info-and-optimisation-levels
category: computing-software
field: software-engineering
product: c
tags: [c, optimisation-levels, debug-symbols, og, o2, strip, separate-debug-info]
level: practitioner
status: docs-checked
description: "Pick -O levels and -g settings, keep separate debug info, and understand why optimised code debugs differently."
sources: ["https://en.cppreference.com/w/c", "https://www.open-std.org/jtc1/sc22/wg14/", "https://gcc.gnu.org/onlinedocs/", "https://clang.llvm.org/docs/UsersManual.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debug info and optimisation levels

Goal: builds you can debug in dev and profile in production.

- `-O0` fastest to compile, easiest to debug; `-Og` optimises while keeping debuggability (GCC); `-O2` is the usual release level; `-O3` adds more inlining/vectorisation; `-Os` favours size.
- `-g` emits DWARF debug info without changing generated code; `-g3` includes macro definitions. Release builds can keep `-g` and strip later.
- Separate debug info: `objcopy --only-keep-debug prog prog.debug; strip --strip-debug prog; objcopy --add-gnu-debuglink=prog.debug prog`. Keep the exact `prog.debug` for each released build.
- Optimised code: variables show `<optimized out>`, lines step out of order, functions inline away. Use `-fno-omit-frame-pointer` for usable profiler and backtrace output, and `-fno-inline` when chasing a specific frame.
- LTO (`-flto`) shifts optimisation to link time; pass the same `-O` flags at link.
- Compare size and speed with `size prog` and a benchmark before choosing `-O3`.

Verify: `gdb prog` shows source lines when built with `-g`.

## Checked

2026-11-02. Confirmed in GCC Debugging Options and Optimize Options and the GDB manual (Separate Debug Files): `-Og` with `-g`, `-g3` includes macro definitions, the `objcopy --only-keep-debug` / `--add-gnu-debuglink` steps, `-fno-omit-frame-pointer`, `-fno-inline`, `-flto`. Removed: the build-id note detail and the `file` output wording.

Method: documentation only; no commands were run.
