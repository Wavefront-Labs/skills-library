---
id: computing-software.software-engineering.nim.osproc-running-commands
name: osproc-running-commands
category: computing-software
field: software-engineering
product: nim
tags: [osproc-running-commands, stdlib-os-and-paths, osproc, execcmd, execcmdex, startprocess, subprocess, shell, pipes, nim]
level: practitioner
status: docs-checked
description: "Run external commands with execProcess, execCmdEx and startProcess, capture output and control streams and exit codes."
sources:
  - https://nim-lang.org/docs/osproc.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running processes with osproc

Goal: invoke child processes safely.

- Quick: `import std/osproc`; `let (output, code) = execCmdEx("git status")`; `execProcess("ls", args = ["-l"], options = {poUsePath})`.
- Streaming: `let p = startProcess("cmd", args = @["a"], options = {poUsePath, poStdErrToStdOut})`; read `p.outputStream`, `p.waitForExit()`, `p.peekExitCode`, `p.close()`.
- Prefer the argument-list form to a shell string to avoid quoting and injection issues; if using a shell string, quote with `quoteShell`.
- `poEvalCommand` passes the command directly to the shell, without quoting; `poParentStreams` uses the parent's streams; `poStdErrToStdOut` merges stderr into stdout; `poUsePath` searches `PATH`. `execProcess` defaults to `{poStdErrToStdOut, poUsePath, poEvalCommand}`, and its doc warns about that default.
- `execCmd(cmd)` returns exit code only; `os.execShellCmd` is the legacy form.
- `countProcessors()` for sizing workers.

Gotchas:
- `close` cleans up handles once the process has finished; on an unfinished process it forcibly terminates it, which may leave zombie processes.
- `waitForExit` on a process created without `poParentStreams` can deadlock if its output buffers fill.

Verify: `execCmdEx("echo hi")` returns ("hi\n", 0) on POSIX.

## Checked

2026-11-02. Confirmed against lib/pure/osproc.nim (all listed procs exist, `ProcessOption` doc comments, `execProcess` defaults, zombie warning, `execCmdEx` returns output and exit code) and lib/pure/os.nim (`quoteShell`, `execShellCmd`). Removed: the memory-buffering claim.
Method: documentation only; no commands were run.
