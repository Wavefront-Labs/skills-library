---
id: computing-software.systems-network-administration.bash.glob-no-match-literal
name: glob-no-match-literal
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, glob-no-match-literal, unmatched-glob, shell-scripting]
level: practitioner
status: docs-checked
description: "Handle bash globs that match nothing, which stay literal by default, using nullglob, failglob or an existence check."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unmatched globs stay literal
**Goal:** avoid processing a literal `*.log` filename.
```bash
for f in *.log; do [[ -e $f ]] || continue; process "$f"; done
shopt -s nullglob; files=(*.log); (( ${#files[@]} )) || echo none
shopt -s failglob      # unmatched glob is an error, command not run
```
- Default: unmatched pattern is passed unchanged, so `rm *.tmp` may try to delete a file named `*.tmp`.
- `nullglob` expands to nothing (then `ls *.x` lists the current dir!); `failglob` aborts the command.
- Scope shopt changes to a function or subshell.
- Self-check: in an empty dir, `echo *.zz` prints `*.zz`; with nullglob prints a blank line.

## Checked

2026-11-02: Confirmed in Filename Expansion (unmatched word left unchanged unless nullglob removes it or failglob prints an error and skips the command) and the shopt option list.
Source read: GNU Bash Reference Manual (https://www.gnu.org/software/bash/manual/bash.html).
Method: documentation only; no commands were run.
