---
id: computing-software.software-engineering.debugging.inspecting-processes-with-proc-lsof-ss
name: inspecting-processes-with-proc-lsof-ss
category: computing-software
field: software-engineering
product: debugging
tags: [debugging, linux, lsof, proc-filesystem, ss, sockets]
level: practitioner
status: docs-checked
description: "Inspect a running Linux process without a debugger via /proc, lsof and ss: unlinked open files, sockets, TCP info and /proc access limits."
sources: ["https://man7.org/linux/man-pages/man5/proc.5.html", "https://man7.org/linux/man-pages/man8/lsof.8.html", "https://man7.org/linux/man-pages/man8/ss.8.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inspecting processes via /proc, lsof and ss

## /proc (proc(5))
- A pseudo-filesystem exposing kernel data structures, normally mounted at `/proc`. `/proc/PID` holds one subdirectory per process, with `task/TID` per thread; `/proc/self` is a link to the caller's own directory. Per-file detail lives in the `proc_pid(5)` pages, which were not read for this skill.
- Many files (environment, command line) use NUL-separated fields; the man page suggests `cat file | tr '\000' '\n'` to read them.
- The mount option `hidepid` (Linux 3.3+) limits who can read `/proc/PID` files: `0` everybody (default), `1` only your own (cmdline and status of others protected), `2` also hides other users' directories. `gid=` exempts a group.

## lsof
```
lsof -p PID        # files opened by that process id
lsof -i :8080      # internet files, here by port
lsof +L1           # open files that have been unlinked (link count < 1)
lsof -u svc        # files of a login name or uid
lsof -c java       # processes whose command begins with the string
lsof -t ...        # terse output: process IDs only
lsof -p PID -a -i  # -a ANDs the selections: that process's internet files
```
- Selection options are ORed unless `-a` is given.
- Link counts are not available for sockets or most FIFOs and pipes. `+L1` selects unlinked open files, and `+aL1 <file_system>` limits that to one file system.

## ss
```
ss -tlnp                 # TCP, listening, numeric, with owning process
ss -tni                  # TCP with internal TCP information
ss -s                    # summary statistics
ss -x -p                 # unix sockets with process
ss -o state established '( dport = :ssh or sport = :ssh )'   # from the man page examples
```
- With no options `ss` lists open non-listening sockets that have established connections.
- `-p` shows processes using sockets, `-T` shows threads (implies `-p`), `-i` shows internal TCP information, `-s` prints summary statistics without parsing socket lists (useful when there are very many sockets).
- Filter syntax is `[ state STATE-FILTER ] [ EXPRESSION ]`; state names include `established`, `syn-sent`, `fin-wait-1`, plus groups such as `connected` and `all`.

## Checked
2026-11-09. Read the full proc(5) page (it is an overview, so the /proc/PID file table, fd counting, limits, stack and wchan claims, queue interpretation and CLOSE_WAIT guidance were removed as unsupported), the lsof options `-a`, `-c`, `-i`, `+L`, `-p`, `-t`, `-u`, and the ss options and state filter sections.
Method: documentation only; no commands were run.
