---
id: computing-software.systems-network-administration.bash.wait-for-pid
name: wait-for-pid
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, wait-for-pid, wait-pid-status, shell-scripting]
level: practitioner
status: docs-checked
description: "Wait for specific background PIDs in bash, collect each exit status, and use wait -n."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Waiting for specific PIDs
**Goal:** run work in parallel and gather results.
```bash
pids=()
for h in "${hosts[@]}"; do check "$h" & pids+=($!); done
rc=0
for p in "${pids[@]}"; do wait "$p" || rc=1; done     # wait PID returns its status
wait -n; echo "first finished: $?"                     # any one job
wait -n -p who                                         # who = id of the job returned
```
- Synopsis: `wait [-fn] [-p varname] [id ...]`. With ids, it returns the exit status of the last id; each id is a PID or jobspec.
- `$!` is the PID of the job most recently placed into the background.
- Plain `wait` with no options or ids waits for all running background jobs (and the last process substitution if its PID is `$!`) and returns zero, hiding failures.
- `wait -n` waits for any one of the ids (or any job or process substitution if none given) and returns its status; the status is 127 if none of the ids is a child of the shell or there are no unwaited-for children.
- `-p varname` assigns the id of the job whose status was returned to varname; it is useful only with `-n`.
- Cap parallelism by calling `wait -n` when the running count reaches N.
- Self-check: `(exit 3) & wait $!; echo $?` prints 3.

## Checked
Method: 2026-11-09 docs-only read of the GNU Bash manual (Job Control Builtins wait, Special Parameters). Confirmed the synopsis, `-n`, `-p`, plain `wait` behaviour, status 127 and `$!`. Removed the version gates (bash 4.3 and 5.1), the once-only wait claim and the `kill -0` polling line for non-child processes, which were not confirmed in the manual.
