---
id: computing-software.systems-network-administration.bash.shopt-lastpipe
name: shopt-lastpipe
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, shopt-lastpipe, lastpipe, shell-scripting]
level: advanced
status: docs-checked
description: "Use shopt -s lastpipe so the last stage of a bash pipeline runs in the current shell and keeps its variables."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# lastpipe and pipeline scope
**Goal:** keep variables set in the final pipeline stage.
```bash
#!/usr/bin/env bash
shopt -s lastpipe
count=0
printf '%s\n' a b c | while read -r x; do (( count++ )); done
echo "$count"        # 3 with lastpipe; 0 without
```
- Each command of a multi-command pipeline normally runs in its own subshell (a separate process), so `... | while read` loses its variables.
- With `lastpipe` set and job control not active, the shell runs the last command of a pipeline (one not run in the background) in the current shell environment. Job control is on by default in interactive shells, so in a terminal run `set +m` first (`-m` enables job control).
- Alternatives: process substitution `while read ...; done < <(cmd)` or a here-string.
- Self-check: output 3 with lastpipe in a script file, 0 when the `shopt` line is removed.

## Checked
2026-11-08: confirmed against the GNU Bash Reference Manual (single-page bash.html): Pipelines (each pipeline command in its own subshell; lastpipe and job control), The Shopt Builtin (lastpipe), and The Set Builtin (-m job control). Removed the "bash 4.2+" claim, which the manual does not state. The `count` output of 3 versus 0 follows from those rules but was not run.
Method: documentation only; no commands were run.
