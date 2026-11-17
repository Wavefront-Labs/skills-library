---
id: computing-software.software-engineering.d.d-process-spawn-and-execute
name: d-process-spawn-and-execute
category: computing-software
field: software-engineering
product: d
tags: [d-process-spawn-and-execute, std-file, std-process, execute, executeshell, spawnprocess, pipeprocess, wait, subprocess, environment, redirect, d]
level: practitioner
status: docs-checked
description: "Run external commands via execute, executeShell, spawnProcess, pipeProcess and wait, with redirection, environment, working directory and exit-status checks."
sources:
  - https://dlang.org/phobos/std_process.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running programs: std.process execute, pipeProcess, spawnProcess

Goal: run subprocesses safely.

- Capture output: `auto r = execute(["git", "status"]); if (r.status != 0) writeln(r.output);`. `execute` waits, and returns `Tuple!(int, "status", string, "output")` with both stdout and stderr captured (`Config.stderrPassThrough` sends stderr to the parent's stderr instead); `maxOutput` caps captured bytes. The array form avoids shell quoting. `executeShell("ls -l")` passes a command string verbatim to the shell, subject to its quoting rules.
- Stream: `auto pid = spawnProcess(["prog", "arg"], stdin, stdout, stderr, env, Config.none, workDir); scope(exit) wait(pid);`. It returns immediately; `wait` returns the exit status. Always `wait` (except for `Config.detached`) to avoid zombie processes. On POSIX a signal death returns a negative status (minus the signal number).
- Pipes: `auto p = pipeProcess(["sort"], Redirect.stdin | Redirect.stdout); p.stdin.writeln("b\na"); p.stdin.close(); foreach (l; p.stdout.byLine) writeln(l); wait(p.pid);`. `Redirect` has `stdin`, `stdout`, `stderr`, `all`, `stderrToStdout`, `stdoutToStderr`. `pipeShell` is the shell variant; `pipe()` makes a bare unidirectional `Pipe`.
- Other: `Config.suppressConsole` (Windows only effect), `Config.newEnv` (child gets only the `env` you pass), `tryWait` (non-blocking, returns `terminated` and `status`), `kill(pid)` (sends SIGTERM on POSIX, forcibly ends on Windows; still `wait` afterwards), `waitTimeout` (Windows only).
- Env: `environment.get("PATH")` (null if missing), `environment["K"] = "v"`, `environment.remove`, `"K" in environment`; pass a `string[string]` map as `env` to add variables for the child (the map wins over the inherited value).
- Errors: `ProcessException` when the process cannot be started or waited on; `escapeShellCommand(args)` and `escapeShellFileName` when building a shell string.

Gotchas:
- A child that reads stdin may wait forever: close (and flush) `p.stdin` before `wait`.
- A `File` that is not one of the parent's standard streams is closed in the parent after `spawnProcess` returns unless you pass a `Config.retainStd*` flag.
- Shell syntax and quoting differ between `cmd.exe` (Windows `nativeShell`) and `/bin/sh` (POSIX).

Verify: unittest executing `["echo", "hi"]` on POSIX or `["cmd","/c","echo hi"]` on Windows.

## Checked

2026-11-08. Confirmed against the std.process page: `execute`/`executeShell` signature and return tuple, `spawnProcess` parameters and examples, `Config` flags, `wait`, `tryWait`, `kill`, `waitTimeout`, `pipeProcess`/`pipeShell`/`Redirect`, `pipe`, `environment` members, `ProcessException`, `escapeShellCommand`, `nativeShell`.

Removed because the page did not confirm it: the deadlock-on-undrained-pipe advice and the `std.concurrency` timeout suggestion; the `Config.suppressConsole` pipeline wording was narrowed to what the page says. Replaced landing-page sources with the std.process page.

Method: documentation only; no commands were run.
