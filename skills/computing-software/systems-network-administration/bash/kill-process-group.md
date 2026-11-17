---
id: computing-software.systems-network-administration.bash.kill-process-group
name: kill-process-group
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, kill-process-group, process-group-kill, shell-scripting]
level: advanced
status: docs-checked
description: "Signal a process group from bash: the kill builtin, job control and set -m, and cleaning up children with an EXIT trap."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Signalling a process group
**Goal:** stop a command and everything it spawned.
```bash
set -m                            # job control: each job gets its own process group
cmd &                             # background job in its own group
kill -TERM %1                     # kill builtin accepts a jobspec
jobs -p                           # PID of each job's process group leader
trap 'echo cleaning up' EXIT      # action runs when the shell exits
```
- The `kill` builtin takes `-s sigspec`, `-n signum` or `-sigspec` plus one or more ids; each id is a jobspec or a pid. With no signal given it sends SIGTERM. It returns zero if at least one signal was sent.
- `set -m` enables job control and runs all processes in a separate process group; a job is a pipeline and all its processes share a process group.
- `jobs -p` lists only the process ID of each job's process group leader; `jobs -x command` replaces any jobspec in the command with the process group ID.
- When job control is on and Bash waits on a foreground command, the shell does not receive keyboard-generated signals because it is not in the terminal's process group.
- Bash mentions `kill 0` as signalling its own group: an interactive Bash ignores SIGTERM so that `kill 0` does not kill it. A non-interactive script is not protected that way.
- `trap '...' EXIT` (or sigspec `0`) runs the action when the shell exits; signals ignored on entry to a non-interactive shell cannot be trapped.
- Negative PIDs to signal a whole group (`kill -- -PGID`), `setsid`, `pkill -P` and `timeout` are not documented in the Bash manual; see kill(1), kill(2) and the tool man pages before relying on them.
- Try TERM first, wait, then escalate.
- Self-check: `jobs` shows no remaining jobs after the kill.

## Checked
Checked 2026-11-08 against the Bash Reference Manual: Job Control Basics, Job Control Builtins (kill, jobs), the `set -m` description, the trap builtin (EXIT) and Signals. Removed because the manual does not cover them: `kill -- -PGID`, setsid, pkill -P, `timeout --foreground`, and the `ps -o` form.

Method: docs-only read of cited pages, 2026-11-08
