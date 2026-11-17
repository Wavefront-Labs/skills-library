---
id: computing-software.systems-network-administration.bash.shell-signals-kill-and-process-management
name: shell-signals-kill-and-process-management
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, sh-kill, signals, background-processes, pgrep-pkill, wait-n]
level: practitioner
status: docs-checked
description: "Start, track and stop background processes from bash scripts with kill, wait, disown, and signal exit statuses."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Process management in scripts

- Start: `cmd & pid=$!`. `$!` expands to the process ID of the job most recently placed into the background (asynchronous command or `bg`).
- `wait "$pid"` waits for that child and returns the exit status of the last id given. With no ids, `wait` waits for all running background jobs (and the last process substitution if its pid equals `$!`) and returns 0. `wait -n` waits for any one of the ids, or any job if none are given, and returns its exit status; the status is 127 if none of the ids is a child of the shell or there are no unwaited-for children. `wait -p varname` stores the id of the finished job (useful with `-n`).
- `kill` sends SIGTERM when no signal is given. Signal names are case-insensitive, with or without the `SIG` prefix: `kill -TERM "$pid"` or `kill -s TERM "$pid"`; ids may be pids or jobspecs. Its status is zero if at least one signal was sent. Try the polite signal first, wait for exit, then escalate.
- `kill -l` lists signal names; `kill -l N` translates a number or a status above 128 to the signal name.
- A command killed by a fatal signal N has exit status 128+N (so 143 is SIGTERM, 137 is SIGKILL, from 128 plus signal numbers 15 and 9).
- If a trap is set for a signal received while bash waits for a foreground command, the trap runs only after that command completes. If bash is in the `wait` builtin, `wait` returns immediately with status above 128 and then the trap runs.
- `disown` removes jobs from the job table; `disown -h` keeps them but stops the shell sending them SIGHUP when the shell receives SIGHUP.
- An interactive bash with no traps ignores SIGTERM (so that `kill 0` does not kill it), always ignores SIGQUIT, and with job control also ignores SIGTTIN, SIGTTOU and SIGTSTP.
- Scripts that start many children should `wait` for them so statuses are collected.

## Checked
2026-11-09. Confirmed in the bash manual: `$!`, `wait` (all forms and statuses), `kill` semantics and `-l`, 128+N status, trap timing, `disown -h`, interactive signal handling. Removed: `kill -0`, process groups with `setsid` / `kill -- -pgid`, `pkill` and `pgrep` advice, PID-file race remarks, `nohup`, `timeout` (and its status 124), the bash 4.3 version tag on `wait -n`, and zombie remarks, which the cited pages do not cover. The signal numbers 9 and 15 are standard but not listed on the cited page.
Method: documentation only; no commands were run.
