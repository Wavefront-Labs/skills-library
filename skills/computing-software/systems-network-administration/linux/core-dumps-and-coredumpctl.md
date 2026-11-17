---
id: computing-software.systems-network-administration.linux.core-dumps-and-coredumpctl
name: core-dumps-and-coredumpctl
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, core-dump, coredumpctl, systemd-coredump, gdb, core-pattern, ulimit-c, debuginfo, abrt, apport, crash-analysis, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Capture and analyse application crashes: enable core dumps (core_pattern, ulimit, systemd-coredump), list and extract them with coredumpctl, and get a usable gdb backtrace."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/coredumpctl.html
  - https://www.freedesktop.org/software/systemd/man/latest/coredump.conf.html
  - https://man7.org/linux/man-pages/man5/core.5.html
  - https://sourceware.org/gdb/current/onlinedocs/gdb.html/Backtrace.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Core dumps, coredumpctl and gdb

**Goal:** when a daemon segfaults, keep the core, get a symbolised backtrace, and hand
developers something actionable.

## 1. Where cores go
```bash
cat /proc/sys/kernel/core_pattern
# |/usr/lib/systemd/systemd-coredump %P %u %g %s %t %c %h ...   piped to systemd-coredump (more % specifiers follow)
# core                                                          file "core" in the process cwd
ulimit -c                       # 0 = disabled for this shell's children
```
- systemd services: `LimitCORE=` in the unit, or `DefaultLimitCORE=` in `system.conf` (see `systemd-system.conf`).
- Shell-launched programs: `ulimit -c unlimited`.
- A set-user-ID program only dumps core if `fs.suid_dumpable` allows it; with value 2 the `core_pattern` must be an absolute path or a pipe (`core(5)`). This has security implications.

## 2. coredumpctl
```bash
coredumpctl list                          # TIME PID UID GID SIG COREFILE EXE
coredumpctl list nginx --since today
coredumpctl info 23145                    # signal, cmdline, cgroup, quick stack trace
coredumpctl dump 23145 -o core.23145      # extract the core file
coredumpctl debug 23145                   # opens gdb with binary + core
```
Storage: `/var/lib/systemd/coredump/` (`Storage=external` is the default); limits in `/etc/systemd/coredump.conf` (`MaxUse=`, `KeepFree=`, `ExternalSizeMax=`). A core larger than `ExternalSizeMax=` (default 32G on 64-bit) is not saved.

## 3. A useful backtrace
```bash
gdb /usr/sbin/nginx core.23145
(gdb) bt full                          # backtrace with locals
(gdb) thread apply all backtrace        # every thread
```

## Gotchas
- Cores can contain secrets (keys, passwords in memory) — restrict access and delete after use.
- Disk: unlimited cores of big JVMs/databases can fill `/var` — set `MaxUse=`.

## Verify
- [ ] `sleep 100 & kill -SEGV $!` produces an entry in `coredumpctl list`.
- [ ] `coredumpctl debug` shows function names (not `??`) in the top frames.

## Checked

2026-10-25, against the systemd v262.1 documentation (man pages and NEWS in the systemd/systemd repository, main branch). Confirmed: `coredumpctl` verbs list/info/dump/debug and `--output=`, `--since`; `coredump.conf` options and the default `Storage=external` in `/var/lib/systemd/coredump/`; `ExternalSizeMax=` defaults; systemd ships `core_pattern` as a pipe to systemd-coredump with extra specifiers and `fs.suid_dumpable=2` (sysctl.d/50-coredump.conf.in); `core(5)` on piping and `suid_dumpable`; `RLIMIT_CORE`; gdb `backtrace full` prints locals and `thread apply all backtrace` covers all threads (gdb manual). Removed distro-specific symbol-package, apport, debuginfod-version and container remarks that no fetched documentation covers.

Method: documentation only; no commands were run.
