---
id: computing-software.software-engineering.debugging.attaching-debuggers-to-running-processes
name: attaching-debuggers-to-running-processes
category: computing-software
field: software-engineering
product: debugging
tags: [debugging, attach-to-process, ptrace-scope, gdb, containers, permissions]
level: practitioner
status: docs-checked
description: "Attach gdb or Visual Studio to a running process: Yama ptrace_scope modes, CAP_SYS_PTRACE, Docker seccomp, detach versus exit."
sources: ["https://www.kernel.org/doc/html/latest/admin-guide/LSM/Yama.html", "https://sourceware.org/gdb/current/onlinedocs/gdb.html/Attach.html", "https://docs.docker.com/engine/security/seccomp/", "https://learn.microsoft.com/en-us/visualstudio/debugger/attach-to-running-processes-with-the-visual-studio-debugger"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Attaching to running processes

## gdb
- `attach process-id` attaches to a process started outside gdb; find the id with `ps` or `jobs -l`. It needs an OS that supports processes and permission to send the process a signal.
- The first thing gdb does is stop the process; you can set breakpoints, step and modify storage, or use `continue` to let it run on.
- If the running executable does not match the loaded exec-file (compared by build ID when available), `set exec-file-mismatch ask|warn|off` decides what happens (default `ask`).
- `detach` releases the process and it continues running. Exiting gdb while attached also detaches; using `run` kills the process. gdb asks for confirmation unless `set confirm` is changed.

## Linux ptrace permissions (Yama)
Yama is a Linux Security Module controlled by `/proc/sys/kernel/yama/ptrace_scope` (writable only with CAP_SYS_PTRACE):
- `0` classic: attach to any process of the same uid, as long as it is dumpable (not changed uid, started privileged, or called `prctl(PR_SET_DUMPABLE)`).
- `1` restricted: by default only descendants, so `gdb EXE` and `strace EXE` work but `gdb --pid=PID` needs CAP_SYS_PTRACE (for example as root). A process can name an allowed debugger with `prctl(PR_SET_PTRACER, ...)`.
- `2` admin-only: only processes with CAP_SYS_PTRACE may use ptrace.
- `3` no attach: no ptrace attach at all, and the value cannot be changed once set.

## Docker
- Docker's default seccomp profile lists `ptrace` as a restricted syscall; tracing arbitrary processes is already blocked by dropping CAP_SYS_PTRACE, because it could leak information from the host.
- `--security-opt seccomp=unconfined` runs a container without the default seccomp profile.

## Visual Studio
- Debug > Attach to Process (Ctrl+Alt+P) attaches to a local or remote process, including apps not started from Visual Studio, and to several processes at once. A remote computer needs the remote debugger (msvsmon.exe) running.

## Checked
2026-11-09. Read the gdb Attach page, the Yama page, the Docker seccomp page (ptrace table row, unconfined) and the Visual Studio attach article. Removed unsupported material: macOS entitlements, WinDbg and SeDebugPrivilege, `kubectl debug` profiles, the combined `--cap-add` command, Ubuntu defaults, TracerPid checks, and production tool suggestions (gcore, procdump, py-spy and others).
Method: documentation only; no commands were run.
