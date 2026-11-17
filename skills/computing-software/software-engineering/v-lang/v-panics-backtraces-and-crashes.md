---
id: computing-software.software-engineering.v-lang.v-panics-backtraces-and-crashes
name: v-panics-backtraces-and-crashes
category: computing-software
field: software-engineering
product: v-lang
tags: [v-panics-backtraces-and-crashes, errors-debugging-and-diagnostics, panic, backtrace, print_backtrace, index out of range, exit code, assert failure, crash, stack trace, runtime error, v-lang]
level: practitioner
status: draft
description: "Understand panic and assert behaviour, get backtraces, differentiate bounds-check failures, and set exit codes deliberately."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Panics, backtraces and error exit codes

Goal: diagnose runtime failures.

- `panic('message')` prints `V panic: message` with a backtrace (when debug info available) and exits with code 1; `assert` failures print the expression and values in debug builds.
- Common runtime panics: array index out of range, map missing key with `or` absent (no panic; returns zero), `none`/error unwrapped with `!` in main, integer division by zero, nil dereference (segfault in unsafe code).
- Manual trace: `print_backtrace()`; builds with `-d no_backtrace` omit them.
- Segfault in release builds: rebuild with `-g -cc clang -cflags -fsanitize=address` (confirm) and rerun.
- Controlled exit: `exit(code)`; in `main`, returning an error from `fn main() !` prints `error: ...` and exits 1 (confirm).
- Recover: V has no exceptions; model recoverable failures with results.

Gotchas:
- Backtraces need `-g` to resolve names (and tcc support varies).
- `-prod` may strip bounds checks only if `@[direct_array_access]` is used; otherwise they stay.

Verify: trigger an out-of-range index and read the trace.
