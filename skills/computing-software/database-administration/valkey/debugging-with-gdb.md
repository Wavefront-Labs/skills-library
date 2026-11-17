---
id: computing-software.database-administration.valkey.debugging-with-gdb
name: debugging-with-gdb
category: computing-software
field: database-administration
product: valkey
tags: [debugging, gdb, core-dump, gcore, backtrace, crash, make-noopt]
level: advanced
status: docs-checked
description: "Debug a Valkey crash with GDB: attach to a running server, make noopt build, bt, info registers, gcore, and what to send developers."
sources:
  - https://valkey.io/topics/debugging/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When a crash report is not enough, GDB lets a user who can reproduce the bug give developers the process state: attach to the running server, wait for the crash, then capture a backtrace and a core file.

Build: Valkey compiles with `-O3` and `-fno-omit-frame-pointer` (precise stack walking). `make noopt` gives an unoptimized binary that is nicer for GDB, but a running production server need not be rebuilt; GDB still works on optimized builds, and Valkey is rarely CPU-bound.

Attach:
1. Find the pid: `valkey-cli info | grep process_id`.
2. Optionally start `screen` or `tmux` so an SSH timeout does not kill the session.
3. `gdb <path-to-valkey-executable> <pid>`, for example `gdb /usr/local/bin/valkey-server 58414`.
4. GDB blocks the server on attach; type `continue` to resume. After that there is no performance loss, so it is safe. Detach screen with Ctrl-a a.

To rehearse, `DEBUG SEGFAULT` simulates a crash (never on production); GDB reports the file and line, better than the built-in report that shows only function names and offsets.

After the crash collect:
- `bt` for the full stack trace.
- `info registers` for the register dump (include both in the bug report).
- `gcore`, which writes a file such as `core.58414`. The core contains all data in memory at crash time, so you are sending your data; developers delete it after use.

Send: the executable, the `bt` output and registers, the core file, and operating system, GCC and Valkey versions.

## Checked
2026-11-03. Confirmed against the Valkey Debugging page (valkey.io/topics/debugging/): default compile flags, `make noopt`, finding the pid with `valkey-cli info`, attaching with `gdb <executable> <pid>` and `continue`, Ctrl-a a to detach screen, `DEBUG SEGFAULT`, `bt`, `info registers`, `gcore` producing `core.<pid>`, the data-exposure warning, and the list of what to send. Nothing removed.
Method: documentation only; no commands were run.
