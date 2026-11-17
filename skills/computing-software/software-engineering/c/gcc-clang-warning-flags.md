---
id: computing-software.software-engineering.c.gcc-clang-warning-flags
name: gcc-clang-warning-flags
category: computing-software
field: software-engineering
product: c
tags: [c, c-toolchain-diagnostics, warning-flags, wall-wextra, wconversion, wshadow, werror]
level: practitioner
status: docs-checked
description: "Choose a strict warning set for GCC and Clang and roll it out without drowning in noise."
sources: ["https://en.cppreference.com/w/c", "https://www.open-std.org/jtc1/sc22/wg14/", "https://gcc.gnu.org/onlinedocs/", "https://clang.llvm.org/docs/UsersManual.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gcc clang warning flags

Goal: let the compiler find bugs before runtime.

- Baseline: `-std=c11 -Wall -Wextra -Wpedantic`. Useful additions: `-Wshadow -Wconversion -Wsign-conversion -Wformat=2 -Wcast-qual -Wstrict-prototypes -Wmissing-prototypes -Wwrite-strings -Wvla -Wundef`.
- Further GCC options: `-Wnull-dereference` (only active when optimisation enables `-fdelete-null-pointer-checks`, so it depends on the `-O` level), `-Wduplicated-cond`, `-Wlogical-op`, `-Wjump-misses-init`; check the Clang manual for which of these Clang supports.
- `-Werror` in CI, not in the shipped build system (new compiler versions add warnings and break downstream builds); or `-Werror=<specific>` for must-fix classes such as `-Werror=implicit-function-declaration`.
- Enable on legacy code incrementally: add one flag, fix or suppress, commit; use `#pragma GCC diagnostic push/ignored/pop` for justified local exceptions, with a comment.
- Third-party headers: add their directory with `-isystem dir` (GCC Directory Options).
- Static analysis complement: `gcc -fanalyzer` (GCC Static Analyzer Options).

Verify: introduce a deliberate sign-compare and unused variable and confirm the build output flags both.

## Checked

2026-11-02. Confirmed in GCC Warning Options, Directory Options, Diagnostic Pragmas and Static Analyzer Options: every named `-W` flag, `-Werror=`, `-isystem`, `#pragma GCC diagnostic push`, `-fanalyzer`, `-Wnull-dereference` needing `-fdelete-null-pointer-checks`. Removed: the GCC-only claim, the GCC 10 version gate, `clang --analyze` and `cppcheck`.

Method: documentation only; no commands were run.
