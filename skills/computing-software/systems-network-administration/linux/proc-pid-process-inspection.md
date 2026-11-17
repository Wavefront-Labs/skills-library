---
id: computing-software.systems-network-administration.linux.proc-pid-process-inspection
name: proc-pid-process-inspection
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, procfs, proc-pid, proc-filesystem, open-files, process-environment, process-limits, deleted-files, lpic-1, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Interrogate a running process through /proc/PID: command line, environment, cwd, open fds and deleted files, limits, status, memory maps, cgroup and namespaces."
sources:
  - https://www.kernel.org/doc/html/latest/filesystems/proc.html
  - https://github.com/mkerrisk/man-pages/blob/master/man5/proc.5
  - https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inspecting a process via /proc/PID

**Goal:** answer "what exactly is this process, what is it using, what config/env did it
start with" with no extra tools — works in minimal containers and rescue shells.

## 1. Identity and launch context
```bash
P=1234
tr '\0' ' ' < /proc/$P/cmdline; echo         # full argv (NUL-separated)
tr '\0' '\n' < /proc/$P/environ              # initial environment from execve (ptrace read permission needed)
readlink /proc/$P/exe                        # binary; "(deleted)" = upgraded on disk, restart needed
readlink /proc/$P/cwd; readlink /proc/$P/root   # working dir, chroot
cat /proc/$P/comm                            # the process's comm value (command name)
```

## 2. State and resources
```bash
grep -E '^(State|PPid|Uid|Gid|Threads|VmRSS|VmSwap|voluntary_ctxt|nonvoluntary_ctxt)' /proc/$P/status
cat /proc/$P/limits                          # soft and hard limit for each resource limit — what the process REALLY got
cat /proc/$P/io                              # I/O accounting: rchar, wchar, read_bytes, write_bytes ...
cat /proc/$P/stack                           # kernel stack (needs CONFIG_STACKTRACE) — where a D-state process is stuck
cat /proc/$P/wchan; echo                     # kernel function it's blocked in (needs CONFIG_KALLSYMS)
cat /proc/$P/cgroup                          # systemd unit / container it belongs to
ls -l /proc/$P/ns/                           # namespace links (see namespaces(7))
cat /proc/$P/oom_score /proc/$P/oom_score_adj
```

## 3. Files and sockets
```bash
ls -l /proc/$P/fd | wc -l                    # open fd count vs limit
ls -l /proc/$P/fd | grep deleted             # deleted files still held open (disk space not freed)
cat /proc/$P/fdinfo/3                        # pos and flags of fd 3 (progress of a long read)
ls -l /proc/$P/fd | grep socket:             # socket inodes → match with ss -p / /proc/net/tcp
```
Entries for unlinked files carry a ` (deleted)` suffix. The fd symlinks can be opened to read the content that is still held open, e.g. `cp /proc/$P/fd/<n> /tmp/recovered`;
writing to them (for example `: > /proc/$P/fd/<n>`) truncates the file, so use it only for logs you do not need.

## 4. Memory
```bash
cat /proc/$P/smaps_rollup                    # Rss, Pss, Shared, Private, Swap totals
cat /proc/$P/maps | awk '{print $6}' | sort -u | head   # mapped libraries/files
```
A mapping whose file was unlinked shows ` (deleted)` after the pathname — for a library this usually means the process still
runs the old version after an update.
Compare `exe`: if the executable was replaced on disk, the link target ends in ` (deleted)`.

## Gotchas
- `/proc/PID/environ` holds the initial environment from `execve`, not later changes.
- Reading another process's `environ`, `fd`, `stack` is governed by ptrace access mode checks (`CAP_SYS_PTRACE` or similar).
- PIDs are reused; re-check `cmdline` before acting on a PID found minutes ago.
- `hidepid=2` (`invisible`) mount option on `/proc` hides other users' `/proc/<pid>` directories.

## Verify
- [ ] Values match `ps` output for the same PID.
- [ ] For deleted-file space issues, `df` drops after the process restarts or the fd is truncated.

## Checked

2026-10-26. Linux kernel proc documentation (torvalds/linux master, 2026-10): /proc/PID entries cmdline, environ, exe, cwd, root, fd, maps, smaps_rollup, stack (CONFIG_STACKTRACE), wchan (CONFIG_KALLSYMS), status fields VmRSS and VmSwap, io accounting fields, oom_score and oom_score_adj, fdinfo, hidepid values. The proc(5) man page (GitHub mirror mkerrisk/man-pages, last commit 2024-05, so older than the current man-pages release): limits, environ as initial environment, exe and maps with the (deleted) suffix, ptrace access mode checks, cgroup membership per cgroup-v2 docs. Removed unconfirmed remarks about 15-character comm, container detection from ns IDs and the needrestart tools.

Method: documentation only; no commands were run.
