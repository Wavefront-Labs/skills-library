---
id: computing-software.systems-network-administration.bash.exec-builtin-replace-shell
name: exec-builtin-replace-shell
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, exec-builtin-replace-shell, exec-replace, shell-scripting]
level: advanced
status: docs-checked
description: "Use bash exec to replace the shell with a program, redirect all later output, and avoid wrapper processes in start scripts."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# exec to replace or redirect
**Goal:** hand over the process or redirect the whole script.
```bash
exec "$@"                          # wrapper script: no extra shell remains
exec > run.log 2>&1                # everything after this goes to the file
exec 3< input.txt                  # open fd without running a command
```
- With a command, exec never returns on success; commands after it run only if exec fails (command not found).
- Without a command, redirections take effect in the current shell.
- If exec cannot run the command, a non-interactive shell exits unless `shopt -s execfail` is set.
- Self-check: `bash -c 'exec echo hi; echo no'` prints only hi.

## Checked

2026-11-02: Confirmed in Bourne Shell Builtins (`exec [-cl] [-a name] [command]`: replaces the shell without a new process; with no command redirections apply to the current shell; non-interactive shell exits if exec fails unless execfail). Removed: env -i, Docker/PID 1, signal-delivery claims; corrected the set -e/execfail claim.
Source read: GNU Bash Reference Manual (https://www.gnu.org/software/bash/manual/bash.html).
Method: documentation only; no commands were run.
