---
id: computing-software.software-engineering.c.gdb-core-dump-analysis
name: gdb-core-dump-analysis
category: computing-software
field: software-engineering
product: c
tags: [c, c-debugging-tools, core-dump, gdb-backtrace, coredumpctl, ulimit-c, postmortem]
level: practitioner
status: docs-checked
description: "Capture a core dump or use coredumpctl and read the crashing backtrace in gdb."
sources: ["https://en.cppreference.com/w/c", "https://www.open-std.org/jtc1/sc22/wg14/", "https://sourceware.org/gdb/documentation/", "https://valgrind.org/docs/manual/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gdb core dump analysis

Goal: find the crash site from a postmortem artifact.

- Enable cores: raise the core-file size limit (`RLIMIT_CORE`, `ulimit -c` in the shell that starts the process). The destination is set by `/proc/sys/kernel/core_pattern`; when it pipes to `systemd-coredump`, list dumps with `coredumpctl list` (see core(5)).
- Open manually: `gdb ./prog core` (the executable must be the exact build that crashed).
- First commands: `bt` (backtrace), `bt full` (locals), `info threads`, `thread apply all bt`, `frame N`, `info locals`, `print *ptr`, `info registers`, `x/16xb addr`.
- Build with `-g`; without symbols you only get addresses (`info symbol addr`). Use the separate debug file when stripped (`set debug-file-directory` or install the -dbg package).

Verify: crash a test program with `raise(SIGSEGV)` and confirm `bt` shows the faulting function and line.

## Checked

2026-11-02. Confirmed in core(5), getrlimit(2), the GDB manual (Backtrace, Memory, Separate Debug Files): `RLIMIT_CORE`, `core_pattern`, `systemd-coredump`, `coredumpctl list`, `set debug-file-directory`. Removed: `coredumpctl gdb/debug`, the container and sanitizer bullets.

Method: documentation only; no commands were run.
