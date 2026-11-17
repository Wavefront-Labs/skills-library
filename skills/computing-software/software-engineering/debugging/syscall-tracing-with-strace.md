---
id: computing-software.software-engineering.debugging.syscall-tracing-with-strace
name: syscall-tracing-with-strace
category: computing-software
field: software-engineering
product: debugging
tags: [debugging, observing-execution, strace, syscall-tracing, ltrace, dtruss, process-monitor, file-not-found, hangs, linux]
level: practitioner
status: docs-checked
description: "Diagnose hangs, missing files, permission errors and slow I/O by tracing system calls with strace (Linux), dtruss/fs_usage (macOS) and Process Monitor (Windows)."
sources: ["https://man7.org/linux/man-pages/man1/strace.1.html", "https://strace.io/", "https://learn.microsoft.com/en-us/sysinternals/downloads/procmon"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# System call tracing with strace

**Goal:** see what a program actually asks the OS for, which answers "which config file
is it reading?", "why does it hang?" and "where does the time go?" without source code.

## Essential invocations
```bash
strace -f -o trace.txt ./app --flag          # follow forks/threads, write to file
strace -f -p <pid>                            # attach to running process (needs ptrace permission)
strace -e trace=openat,stat,access ./app      # only file lookups
strace -e trace=%file,%network -f ./app       # syscall classes: %file %network %process %signal %memory
strace -f -e trace=openat -e status=failed ./app   # only failing calls
strace -c -f ./app                            # summary table: count, errors, time per syscall
strace -T -tt -f ./app                        # time spent in each call + timestamps
strace -s 256 -yy ./app                       # longer strings; decode fds to paths/sockets
```

## Recipes
- **Which file/config is missing?** `-e trace=%file -e status=failed` shows
  `openat(..., "/etc/app/conf.yaml", ...) = -1 ENOENT`.
- **Permission denied**: look for `EACCES`/`EPERM` and the exact path.
- **Hang**: attach with `-p`; the last line shows the call it is blocked in; `-yy`
  decodes file descriptors to paths or sockets.
- **Slow startup**: `-c` and `-T` show which calls take the time or fail repeatedly.
- **What does it exec?** `-e trace=execve -f` shows every spawned command with args.

## Caveats
- Attaching with `-p` needs ptrace permission; see the strace man page and your
  system's ptrace restrictions. Tracing changes timing, so timing-sensitive bugs may shift.

## Other OSes
- Windows: Sysinternals Process Monitor (see its page for filters).

## Verify
- [ ] The failing syscall and its errno identified and matched to the observed symptom.

## Checked
2026-11-01. Confirmed against the strace(1) man page: `-f`, `-o`, `-p`, `-e trace=` classes `%file %network %process %signal %memory`, `-e status=` (failed), `-c`, `-T`, `-tt`, `-s`, `-yy` (decode fds). Removed: version gate, ltrace reliability, eBPF tool names, container capability, Yama sysctl and the macOS dtruss/fs_usage lines, syscall interpretations (futex, port 53, fsync).
Method: documentation only; no commands were run.
