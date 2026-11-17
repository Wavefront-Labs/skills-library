---
id: computing-software.systems-network-administration.bash.redirect-both-streams
name: redirect-both-streams
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, redirect-both-streams, stderr-to-stdout, shell-scripting]
level: practitioner
status: docs-checked
description: "Redirect stdout and stderr together in bash with 2>&1 ordering, &> and |& and avoid the common ordering mistake."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
  - https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Redirect stdout and stderr together
**Goal:** capture both streams to one place.
```bash
cmd > all.log 2>&1       # stdout to file, THEN stderr to same place
cmd &> all.log           # bash shorthand; &>> appends
cmd 2>&1 | cat > all.log   # or: cmd |& cat > all.log
cmd 2>&1 > out.txt       # WRONG order: stderr goes to the terminal
cmd >/dev/null 2>&1      # silence everything
```
- Redirections apply left to right: `2>&1` copies where fd1 points NOW.
- Self-check: `{ echo o; echo e >&2; } > f 2>&1; wc -l < f` prints 2.

## Checked

2026-11-02: Confirmed in Redirections (`&>word` and `&>>word` redirect both stdout and stderr, order of redirections matters, left to right) and Pipelines (`|&` pipes stderr too). Removed: sh portability, buffering and tee claims.
Source read: GNU Bash Reference Manual (https://www.gnu.org/software/bash/manual/bash.html).
Method: documentation only; no commands were run.
