---
id: computing-software.systems-network-administration.linux.attach-gdb-to-a-live-process
name: attach-gdb-to-a-live-process
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, gdb-attach, pstack, gdb, gcore, debuginfod, hung-process, stack-trace, ptrace-scope]
level: advanced
status: docs-checked
description: "Get stack traces from a hung or spinning process with gdb attach, debuginfod symbols, ptrace_scope limits and minimal pause impact."
sources:
  - https://sourceware.org/gdb/current/onlinedocs/gdb.html/Attach.html
  - https://sourceware.org/elfutils/Debuginfod.html
  - https://docs.kernel.org/admin-guide/LSM/Yama.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Attaching gdb to a live process

**Goal:** see what a stuck or CPU-spinning process is doing now, without killing it.

## One-shot backtrace (all threads)
```bash
gdb -p 4211 -batch -ex 'set pagination off' -ex 'thread apply all bt' > bt.4211.txt 2>&1
```
GDB stops the process when it attaches. In batch mode gdb detaches on exit, which lets the process
continue. Take several samples a few seconds apart: identical frames suggest it is stuck there; changing
frames suggest a busy loop.

## Symbols
Without debug info frames show as `?? ()`. Add debuginfod servers to the `DEBUGINFOD_URLS` environment
variable (space-separated URLs) so debuginfod-aware tools can fetch symbols on demand.

## Permission problems
`ptrace: Operation not permitted` can come from Yama `kernel.yama.ptrace_scope`:
- 0: classic ptrace permissions (same uid, process dumpable).
- 1: restricted; only descendants may be attached to (so `gdb --pid=PID` needs root or `CAP_SYS_PTRACE`).
- 2: admin-only attach (`CAP_SYS_PTRACE`).
- 3: no attach; once set it cannot be changed.
Containers and SELinux policy can also block ptrace; check your distribution's documentation.

## Gotchas
- Never leave gdb attached interactively on production: the process is stopped until you continue or
  `detach`.
- Exiting gdb with an attached process detaches it; using `run` kills it.

## Verify
- [ ] Backtrace has resolved function names; multiple samples identify the hot or blocked frame.

## Checked
2026-10-28. Confirmed in the gdb manual (Attach): attach stops the process, `detach` continues it, exiting
gdb detaches; in the elfutils debuginfod page: `DEBUGINFOD_URLS`, space-separated; in the kernel Yama page:
`ptrace_scope` values 0-3 and `CAP_SYS_PTRACE`. Removed (not confirmed): eu-stack, pstack, gcore, ddebs
and debuginfo-install package steps, per-distro debuginfod server claims, py-spy, jstack and node tooling,
the `deny_ptrace` SELinux boolean, `/proc/PID/stack`.
Method: documentation only; no commands were run.
