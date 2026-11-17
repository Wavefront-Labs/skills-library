---
id: computing-software.systems-network-administration.bash.pid-and-bang-parameters
name: pid-and-bang-parameters
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, pid-and-bang-parameters, bashpid, shell-scripting]
level: practitioner
status: docs-checked
description: "Use $$, $!, $BASHPID and $PPID correctly: script PID, last background PID, subshell PID and parent PID."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
  - https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PID parameters $$ $! $BASHPID
**Goal:** identify the right process.
```bash
echo "script pid $$"             # in a subshell this is still the invoking shell's pid
( echo "$$ vs $BASHPID" )        # BASHPID differs inside a subshell
: & bgpid=$!                      # pid of the most recent background job
wait "$bgpid"; echo "status $?"
echo "parent $PPID"
```
- `$!` is empty until a background job has been started; capture it immediately.
- Self-check: `( [ "$$" != "$BASHPID" ] && echo sub )` prints sub.

## Checked

2026-11-02: Confirmed in Special Parameters (`$$` is the invoking shell pid even in a subshell; `$!` pid of the most recent background job), Bash Variables (BASHPID differs from $$ in subshells; PPID) and Builtins (`wait`). Removed: version, process-group kill, temp-file predictability claims, sleep example.
Source read: GNU Bash Reference Manual (https://www.gnu.org/software/bash/manual/bash.html).
Method: documentation only; no commands were run.
