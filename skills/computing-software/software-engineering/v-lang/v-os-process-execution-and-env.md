---
id: computing-software.software-engineering.v-lang.v-os-process-execution-and-env
name: v-os-process-execution-and-env
category: computing-software
field: software-engineering
product: v-lang
tags: [v-os-process-execution-and-env, os-module, os.execute, os.system, process, os.process, exec, getenv, setenv, exit code, command, v-lang]
level: practitioner
status: docs-checked
description: "Run commands with os.execute and os.Command or os.Process, capture output, read and set env vars and exit codes."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running processes and environment variables

Goal: shell out safely.

- Simple: `r := os.execute('git status')`; `r.exit_code`, `r.output` (`os.Result`).
- Fire and forget: `os.system('make')` returns an `int` exit code.
- Streaming: `mut p := os.new_process('/bin/ls'); p.set_args(['-l']); p.set_redirect_stdio(); p.run(); for p.is_alive() { line := p.stdout_read() ... }; p.close()`.
- Environment: `os.getenv('HOME')`, `os.getenv_opt('X')`, `os.setenv('K', 'v', true)`, `os.environ()`.
- Exit: `exit(2)`; `os.signal_opt(.int, handler)!` installs a signal handler (`signal_opt(signum Signal, handler SignalHandler) !SignalHandler`).
- Find programs: `os.find_abs_path_of_executable('git')!`.

Gotchas:
- `os.execute` takes one command string; never interpolate untrusted input into it. Pass arguments separately with `os.new_process(...)` and `set_args`.

Verify: run `echo hi` and assert output trimmed equals `hi`.

## Checked

2026-11-03. Confirmed against the V repository source (vlib modules and doc/docs.md) read in this batch: os.execute returning os.Result (exit_code, output), os.system, new_process, Process set_args/set_redirect_stdio/run/is_alive/stdout_read, getenv/getenv_opt/setenv(name, value, overwrite)/environ, find_abs_path_of_executable, signal_opt (vlib/os).
Removed or corrected: 'Failure to start is reported via exit code', 'goes through a shell on some platforms', the path-quoting gotcha and '(confirm signature)'.
Method: documentation only; no commands were run.
