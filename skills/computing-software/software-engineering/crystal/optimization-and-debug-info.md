---
id: computing-software.software-engineering.crystal.optimization-and-debug-info
name: optimization-and-debug-info
category: computing-software
field: software-engineering
product: crystal
tags: [optimization-and-debug-info, llvm-backend, optimization, o3, debug-symbols, debug-info, crystal]
level: advanced
status: docs-checked
description: "Choose Crystal optimization levels -O0 to -O3, -Os and -Oz, --release and --single-module, and control symbolic debug info with --debug and --no-debug."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/man/crystal/README.md
  - https://github.com/crystal-lang/crystal/blob/master/src/compiler/crystal/command.cr
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Optimisation levels and debug info

Goal: balance speed, size and debuggability.

- The optimisation level sets the codegen effort: a trade-off between compile time (worse with higher levels) and runtime performance (better). Production builds should usually use the highest level.
- `-O0` none (default), `-O1` low, `-O2` middle, `-O3` high, `-Os` middle with focus on file size, `-Oz` middle aggressively focused on size.
- `--release` is equivalent to `-O3 --single-module`, and gives the best results; `--single-module` generates one LLVM module.
- `-d` / `--debug` adds full symbolic debug info; `--no-debug` skips it, reducing the output size but making debugging harder.
- Non-release builds are much faster to compile and still perform reasonably well, so there is usually no reason to use `--release` for development.

Gotchas:
- Use `--release` when benchmarking.
- For smaller distributable files, use `--no-debug`.

Verify: build with `-O0` and with `--release` and compare compile time and binary size.

## Checked

2026-11-03. Confirmed against the Crystal compiler manual (Release builds, Optimizations) and the command source (`-O` values `0, 1, 2, 3, s, z`, `--release`, `--single-module`, `--debug`, `--no-debug`).
Removed: gdb/lldb breakpoint advice, `strip`, binary-size figures, `p!`/`pp!` debugging notes, backtrace and undefined-behaviour claims, and LLVM-version advice (none appear in the pages read). The description was rewritten to match.
Method: documentation only; no commands were run.
