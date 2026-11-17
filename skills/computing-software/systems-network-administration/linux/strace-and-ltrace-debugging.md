---
id: computing-software.systems-network-administration.linux.strace-and-ltrace-debugging
name: strace-and-ltrace-debugging
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, strace, ltrace, strace-e, strace-follow, syscall, debugging, troubleshooting, ptrace, attach-pid, latency, enoent, eacces, hung-process, sysadmin, performance-troubleshooting]
level: advanced
status: docs-checked
description: "Diagnose a hung, slow, or failing process by tracing its syscalls (strace) and library calls (ltrace), with the flags that matter in production."
sources:
  - https://github.com/strace/strace/blob/master/doc/strace.1.in
  - https://github.com/dkogan/ltrace/blob/master/ltrace.1
  - https://www.kernel.org/doc/html/latest/admin-guide/LSM/Yama.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# strace and ltrace — watch exactly what a process asks the kernel for

**Goal:** when a process hangs, errors with no useful message, or is
mysteriously slow, trace its actual syscalls to see the real file it opened,
the real error code it got back, or exactly where it's blocked — without
needing source code or a debug build.

## 1. strace basics — syscalls
```bash
strace -f -e trace=open,openat,read,write -p <PID>    # attach to a running process
strace -f -o trace.log ./myprogram arg1 arg2            # run fresh, save to file
strace -tt -f -o trace.log -p <PID>                     # -tt = microsecond timestamps, essential for latency work
```
`-f` (`--follow-forks`) traces child processes as they are created — without it a multi-process app's trace shows
nothing useful past the first `fork()`. `-e trace=<set>` filters to a
syscall class (`%file`, `%network`, `%process`, `%signal`; the form without `%` is deprecated),
or names specific calls — tracing everything on a busy process is both slow
and unreadable.

## 2. The highest-value pattern: find the failing syscall
```bash
strace -f -e trace=%file ./myprogram 2>&1 | grep -E 'ENOENT|EACCES|ENOTDIR'
```
"Program X fails with no useful error" often resolves to
one line in the trace: `open("/etc/myapp/config.yml", O_RDONLY) = -1 ENOENT
(No such file or directory)` — the wrong path, a missing file, or a
permission the app's own error message never surfaced. This is almost
always faster than reading application logs or source when the failure is
at the OS-interaction boundary (file, network, permissions) rather than in
application logic.

## 3. Timing — find what's actually slow
```bash
strace -c -f ./myprogram                 # summary: syscall, count, total time, % time — the profile, not the trace
strace -T -f -p <PID>                     # shows the time spent in each system call
```
`-c` is the fastest way to answer "is this process spending its time in
syscalls at all, or in userspace computation" — a high percentage in
`read`/`recvfrom`/`futex` points at I/O or lock contention; near-zero
syscall time with the process still slow means the bottleneck is in
userspace (CPU-bound code, GC, algorithmic) and `perf` is the better tool
(see `computing-software.systems-network-administration.linux.perf-profiling`).

## 4. Diagnosing a hang
```bash
strace -p <PID>                           # attach to a stuck process; the LAST line printed is where it's blocked
```
If the trace shows nothing moving and the last syscall is `futex(...,
FUTEX_WAIT, ...)`, the process is blocked on a lock — check what else holds
it. `read(fd, ...)` with nothing following means it's blocked waiting on
data from that fd (a socket with no data, a pipe with nothing written,
a FIFO with no reader) — `lsof -p <PID>` to see what that fd actually is.
`select`/`poll`/`epoll_wait` sitting with no return means it's waiting on
an event that never arrives — check the other end of whatever it's waiting on.

## 5. ltrace — library calls (one layer up from syscalls)
```bash
ltrace -f -e 'malloc+free+strcpy' -p <PID>
ltrace -S ./myprogram        # -S interleaves syscalls too, for the full picture
```
ltrace traces dynamic library calls (`malloc`, `strcpy`, anything in a
shared `.so`), useful when the bug is in library-level logic rather than a
kernel interaction. Reach for strace first; use ltrace only once strace
confirms the issue isn't at the syscall boundary.

## 6. Production-safe usage
- A traced process runs more slowly than an untraced one (strace(1); `--seccomp-bpf` can reduce the impact);
  never leave it attached to a latency-sensitive production process longer than needed, and prefer
  `-c` (summary) over a full trace when just sizing the problem.
- `strace` needs `ptrace` permission. Where `CAP_SYS_PTRACE` is dropped or a seccomp profile blocks
  `ptrace()`, attaching fails with `Operation not permitted`; add the capability for the debug session or
  trace from the host against the host-visible PID.
- The Yama LSM sysctl `kernel.yama.ptrace_scope` restricts attaching: 0 classic same-uid rules, 1 only descendants
  (unless allowed by the inferior), 2 only `CAP_SYS_PTRACE`, 3 no attach, and 3 cannot be changed once set (kernel Yama documentation).

## Gotchas
- A trace with `-f` on a process that forks very frequently (web servers,
  build systems) generates enormous output fast — pipe through `grep`/`-e
  trace=` filters rather than capturing everything then searching after.
- Signal delivery (`strace -e signal`) shows a process receiving `SIGTERM`/
  `SIGKILL` it's not handling as "exited" in its own logs — useful for the
  "why did this just silently die" class of bug that application logs
  never explain because the process never got to log anything.
- `-tt` prints wall-clock time with microsecond precision; `-T` shows the time spent in each call — use `-T` for per-call latency.

## Verify
- [ ] The specific failing syscall (with its exact errno) is identified in the trace, not just "something failed."
- [ ] `strace -c` summary points at the right subsystem (I/O vs compute) before escalating to `perf`.
- [ ] Tracing was removed/detached from any production process once the diagnosis is captured — not left running.
- [ ] If tracing a containerized process, the capability/seccomp requirement needed to attach is documented for next time.

## Checked
2026-10-27. Checked against the strace(1) manual source (strace/strace, current master) and the ltrace(1) manual source (dkogan/ltrace), the Linux kernel Yama documentation and kernel docs. Confirmed: -f/--follow-forks, -c summary, -p with PIDs, -tt wall-clock microseconds, -T time in each call, trace sets %file, %network, %process, %signal (the plain forms are deprecated), the note that traced processes run slower with --seccomp-bpf as mitigation; ltrace -f, -S and the -e symbol+symbol filter syntax; Yama ptrace_scope values 0 to 3. Changed: trace=file and similar to the documented %file forms. Removed: the 2-20x slowdown figure, the 'nine times out of ten' claim, Docker and Kubernetes default claims, the ltrace reliability claim and the NTP remark, which the documents do not cover.

Method: documentation only; no commands were run.
