---
id: computing-software.software-engineering.debugging.diagnosing-hung-processes
name: diagnosing-hung-processes
category: computing-software
field: software-engineering
product: debugging
tags: [debugging, hung-process, process-hang, deadlock, thread-dump]
level: advanced
status: docs-checked
description: "Diagnose a hung process: collect stacks non-destructively (py-spy dump, dotnet-dump) and classify the hang as deadlock, blocked I/O, livelock or starvation."
sources: ["https://man7.org/linux/man-pages/man5/proc.5.html", "https://github.com/benfred/py-spy", "https://learn.microsoft.com/en-us/dotnet/core/diagnostics/debug-deadlock"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnosing hung processes

## 1. What kind of "hung"?
- Low CPU means the process is waiting (lock, I/O, network, sleep); high CPU means a busy loop, livelock or GC
  thrash. Check per-thread CPU with your platform's tools before choosing a collection method.
- Is it every request or only some? Does a health endpoint respond?

## 2. Collect stacks (several, seconds apart, before restarting)
- **Python**: `py-spy dump --pid PID` prints a single call stack of where a Python program is hung. `--locals`
  adds local variables per frame, `--native` includes C/C++/Cython extension frames (best with symbols).
  On Linux, attaching to a non-child process usually requires root unless the `ptrace_scope` sysctl is
  relaxed. In Docker add `--cap-add SYS_PTRACE`; Kubernetes drops `SYS_PTRACE` by default, so grant it
  (for example through an ephemeral container profile).
- **.NET** (Microsoft deadlock tutorial): `dotnet-dump collect -p PID` (use `sudo` if needed), then
  `dotnet-dump analyze <core file>`; at the prompt `threads` lists all threads and `clrstack -all` prints the
  call stacks of every thread. A deadlocked ASP.NET Core app showed over 300 threads accumulating.
  `dotnet-trace ps` lists processes.
- **Linux per-thread view**: `/proc/<pid>/task/<tid>/` has one directory per thread (see proc(5)).
- For JVM, Go and native stacks look up the runtime's own thread-dump tooling; the sources here do not cover them.

Compare several dumps: threads stuck on the same frame in every dump are the hang.

## 3. Classify
- **Deadlock**: threads each holding a lock and waiting for another's. Fix lock ordering, use timeouts,
  reduce lock scope.
- **Blocked on external I/O**: stacks in socket read, a database driver or an HTTP client usually mean
  missing timeouts; check the connection and the remote side.
- **Pool exhaustion / starvation**: all workers waiting on a pool or on tasks queued behind the same pool
  (blocking on async results from the same executor).
- **Livelock / busy loop**: high CPU, stacks change but stay in the same loop; profile (py-spy has `top` and
  `record` modes).

## 4. Prevent
Timeouts on every external call and lock acquisition, liveness probes that detect stuck workers, bounded
queues, and automatic thread dumps on health-check failure.

## Checked
2026-11-09. Confirmed against the py-spy README (`dump`, `--pid`, `--locals`, `--native`, root and
`ptrace_scope`, `SYS_PTRACE` in Docker and Kubernetes), the Microsoft "Debug a deadlock in .NET Core"
tutorial (`dotnet-dump collect/analyze`, `threads`, `clrstack -all`, `dotnet-trace ps`) and proc(5)
(`/proc/pid/task/tid`). Removed as not stated in these pages: `top -H`/`pidstat`, `/proc` State letters and
D-state advice, jcmd/jstack/kill -3, dotnet-stack, faulthandler, Go pprof, gdb/eu-stack/gcore,
`/proc/PID/stack`, wchan and sysrq, `ss`, `perf top`, `jstat` and `iostat`. The Oracle Java hang page
redirected to a landing page and was not usable.
Method: documentation only; no commands were run.
