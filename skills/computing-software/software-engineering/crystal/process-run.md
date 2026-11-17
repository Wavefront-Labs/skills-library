---
id: computing-software.software-engineering.crystal.process-run
name: process-run
category: computing-software
field: software-engineering
product: crystal
tags: [process-run, process-system, process, subprocess, exit-status, capture-output, shell-command, backtick, process-new, spawn-process, crystal]
level: practitioner
status: docs-checked
description: "Run subprocesses with Process.run, capture output, pass env and stdin, use shell vs direct args, and handle exit status."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/crystal/tree/master/src
  - https://github.com/crystal-lang/crystal-book/tree/master/docs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running external commands with Process

Goal: call other programs safely.

```crystal
out = IO::Memory.new
err = IO::Memory.new
st = Process.run("git", ["rev-parse", "HEAD"], output: out, error: err)
st.success?; st.exit_code
```
- Args are passed as an Array, no shell; `shell: true` runs through `sh -c` (avoid with untrusted strings).
- Options: `env: {"K" => "v"}`, `clear_env: true`, `chdir:`, `input: IO|Process::Redirect::Pipe|Close|Inherit`, `output:`, `error:`.
- Async: `p = Process.new(cmd, args, output: Process::Redirect::Pipe)`; read `p.output`; `p.wait`; `p.terminate`/`signal`.
- Replace the current process: `Process.exec` (raises `IO::Error` if it fails).
- Failure to execute (for example a missing binary) raises `IO::Error`; `Process.run?` is the non-raising variant for argument lists.
- Pid/info: `Process.pid`, `Process.find_executable("git")`.

Gotchas:
- Deadlock if you pipe both stdout and stderr and read only one; use IO::Memory sinks.
- Never interpolate user input into a shell string.
- There is no `Process.fork` in the standard library.

Verify: run `echo` and check captured output.

## Checked

Date 2026-11-03. Confirmed in the Process, Process::Status and executable_path source: Process.run overloads with env, clear_env, chdir, shell, input, output, error, Process.run?, Process.exec, Process.pid, Process.signal, Process.find_executable, Process#wait, signal and terminate, Process::Status#success? and exit_code, and the IO::Error raised when execution fails. Removed the '(confirm)' fork hedge and the File::NotFoundError claim.

Method: documentation only; no commands were run.
