---
id: computing-software.systems-network-administration.bash.tee-log-file-exec
name: tee-log-file-exec
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, tee-log-file-exec, exec-tee, shell-scripting]
level: practitioner
status: docs-checked
description: "Log all output of a bash script to a file while still showing it on screen, using exec with tee process substitution."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logging all output with exec and tee
**Goal:** console and file get the same output with no per-command redirects.
```bash
log=/var/log/myjob.log
exec > >(tee -a "$log") 2>&1
echo "starting"
# separate files:
exec > >(tee -a out.log) 2> >(tee -a err.log >&2)
```
- `exec` with no command, only redirections, changes the redirections of the current shell; the status is zero if there are no redirection errors.
- `>(list)` is process substitution: writing to the file provides input to list, which runs asynchronously, so the tee process is not waited for automatically.
- `$!` is the PID of the most recent background job. Plain `wait` also waits for the last process substitution when its PID is the same as `$!`, which lets the script wait for tee to flush before exiting.
- Use a fresh or datestamped log name per run and rotate long-lived logs.
- Self-check: the same lines appear on screen and in the log file.

## Checked
Method: 2026-11-09 docs-only read of the GNU Bash manual (Bourne Shell Builtins exec, Process Substitution, Job Control Builtins wait, Special Parameters). Confirmed exec-with-redirections, process substitution semantics and the `wait` rule for the last process substitution. Removed the bash 4.4 gate, the sleep workaround, the cron and logrotate remarks, and the timestamp loop and moreutils `ts` suggestions, which were not confirmed in the manual.
