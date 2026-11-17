---
id: computing-software.software-engineering.fortran.execute-command-line
name: execute-command-line
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, execute-command-line, fortran-cmdline-env]
level: practitioner
status: docs-checked
description: "Run shell commands with execute_command_line and check exitstat and cmdstat; avoid injection."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# execute_command_line
**Goal:** call external commands.
```fortran
integer :: exit_code, cmd_stat
call execute_command_line('ls -l', wait=.true., exitstat=exit_code, cmdstat=cmd_stat)
if (cmd_stat /= 0 .or. exit_code /= 0) print *, 'command failed'
```
- `execute_command_line(command [, wait, exitstat, cmdstat, cmdmsg])` runs a shell command, synchronously or asynchronously.
- The command is passed to the shell (`sh` on Unix systems, `cmd.exe` on Windows); if `wait` is present and false the command runs asynchronously where supported, otherwise it runs synchronously through the C library `system` call.
- After synchronous execution `exitstat` holds the exit code as returned by `system`; `cmdstat` is zero if the command line was executed, whatever its exit status; `cmdmsg` receives an error message.
- The manual notes `system` need not be thread-safe, so do not call it concurrently.
## Gotchas
- The command is interpreted by the shell, so building it from untrusted input allows shell injection; avoid it or validate input.
## Self-check
Run a command that exits with a known non-zero status and confirm `exit_code` reports it.

## Checked
2026-11-02. Confirmed in intrinsic.texi: EXECUTE_COMMAND_LINE synopsis, shell used (sh / cmd.exe), asynchronous fallback to system, exitstat/cmdstat/cmdmsg semantics, thread-safety note. Removed: 'standard since F2008', exitstat undefined when asynchronous, flush advice (not stated on the page read).
Method: documentation only; no commands were run.
