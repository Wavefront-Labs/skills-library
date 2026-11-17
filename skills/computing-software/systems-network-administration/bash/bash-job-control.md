---
id: computing-software.systems-network-administration.bash.bash-job-control
name: bash-job-control
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, linux, job-control, bg-fg, jobs, ctrl-z, sigstop, sigcont, wait, background-jobs, jobspec, kill-percent, huponexit, process-management, lpic-1, lfcs, sysadmin]
level: practitioner
status: docs-checked
description: "Use bash job control: Ctrl-Z/bg/fg/jobs, %-jobspecs, wait and wait -n, kill %1, stopped-job warnings on exit, set -m in scripts, and background jobs at shell exit."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html#Job-Control
  - https://man7.org/linux/man-pages/man7/signal.7.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Job control — suspending, backgrounding and waiting on processes from one shell

**Goal:** juggle several commands in one terminal, suspend an editor to run something,
park a long job in the background, and collect its exit status.

## 1. The basics
```bash
long-cmd &            # start in background; prints [1] 12345 (job number, PID)
jobs -l               # list with PIDs and states (Running/Stopped/Done)
Ctrl-Z                # suspend the foreground job (SIGTSTP) → "Stopped"
bg                    # resume the most recent stopped job in the background (SIGCONT)
fg %2                 # bring job 2 to the foreground
kill %1               # SIGTERM to job 1;  kill -STOP %1 / kill -CONT %1
wait                  # block until ALL background jobs finish
wait %1; echo $?      # exit status of a specific job
```
Jobspecs: `%n` number, `%str` command starts with str, `%?str` contains, `%%`/`%+` current,
`%-` previous. A bare `fg`/`bg`/`kill %` defaults to the current job (`+` in `jobs`).

## 2. Stopped jobs and the terminal
- A background job that tries to **read** the terminal is stopped (SIGTTIN); one that
  writes is allowed unless `stty tostop`. `fg` it to interact.
- `exit` with stopped jobs warns once ("There are stopped jobs"); a second `exit` kills
  them. Check `jobs` first.
- On SIGHUP an interactive shell resends SIGHUP to all jobs (sending SIGCONT first to stopped ones);
  `disown` removes a job from the table and `disown -h` marks it so it gets no SIGHUP. With `shopt -s huponexit`
  an interactive login shell also sends SIGHUP to all jobs when it exits.

## 3. Waiting in scripts
```bash
set -m                # enable job control (monitor mode); without it kill and wait take PIDs, not %jobspecs
for h in "${hosts[@]}"; do ssh -n "$h" uptime > "out/$h" & done
wait                  # all
fail=0; for p in "${pids[@]}"; do wait "$p" || fail=1; done

# react as each finishes
pids=(); for f in *.csv; do process "$f" & pids+=($!); done
while (( ${#pids[@]} )); do wait -n; ...; done     # wait -n -p var stores the finished job's PID

# bounded parallelism
for f in *.png; do (( $(jobs -rp | wc -l) >= 4 )) && wait -n; optipng "$f" & done; wait
```
`$!` is the PID of the last background command — save it immediately. `wait` on a PID that
is not a child of this shell returns 127.

## 4. Signals involved
Ctrl-Z → the suspend character, stops the foreground job. SIGSTOP (`kill -STOP`) can stop a
process not tied to your terminal and cannot be caught. Keyboard signals such as SIGINT go to the
foreground **process group**, and all processes of a pipeline belong to one job.

## Failure modes
- `fg`/`bg` fail in a script because job control is off: add `set -m` or use PIDs with `wait`.
- Job stopped immediately after `&`: it reads the terminal (SIGTTIN) — redirect `< /dev/null`.
- Exit status lost: `wait` without arguments returns 0 regardless; wait per PID.
- Background job output garbles the prompt: redirect to a file, or `stty tostop` to pause it.
- Jobs get SIGHUP when the shell receives SIGHUP: `disown -h` the job for anything long.

## Verify
- [ ] `sleep 100 &`, `jobs`, `kill %1`, `jobs` shows Terminated — the jobspec addressed the right job.
- [ ] A script with two background `false`/`true` jobs and per-PID `wait` reports exit 1 for the failing one.

## Checked
2026-11-01. Confirmed against the Bash Reference Manual (Job Control, Signals) and signal(7): jobspecs, bg/fg/jobs/kill/wait/disown
behaviour, `wait -n`/`-p`, exit status 127, SIGTTIN/`stty tostop`, stopped-jobs warning, huponexit, `set -m`.
Removed: version gates, ssh escape, tmux note, nohup/setsid/systemd-run advice, exact error text.
Method: documentation only; no commands were run.
