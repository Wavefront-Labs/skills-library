---
id: computing-software.systems-network-administration.bash.subshell-variable-loss
name: subshell-variable-loss
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, subshell-variable-loss, subshell-scope-bug, shell-scripting]
level: practitioner
status: docs-checked
description: "Find and fix variables lost in bash subshells: pipelines, command substitution, parentheses and background jobs."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Variables lost in subshells
**Goal:** recognise subshell boundaries.
```bash
n=0; printf '%s\n' a b | while read -r x; do n=$((n+1)); done; echo "$n"   # 0
n=0; while read -r x; do n=$((n+1)); done < <(printf '%s\n' a b); echo "$n" # 2
n=0; ( n=5 ); echo $n      # 0
out=$(n=5); echo $n        # 0
```
- Subshell cases: each command of a multi-command pipeline (it runs in its own subshell), `( list )`, command substitution `$( )`, asynchronous commands `&`. Process substitution `<( )` also runs the list asynchronously.
- Fixes: feed the loop with process substitution (`done < <(cmd)`) or a here-string, `shopt -s lastpipe` (the last pipeline element may then run in the current shell, only when job control is not active), write results to stdout or a temp file, use `mapfile` to collect lines.
- Variable changes made in a subshell do not reach the parent.
- Self-check: the first form prints 0, the second 2.

## Checked
Method: 2026-11-09 docs-only read of the GNU Bash manual (Pipelines, Command Grouping, Command Substitution, Process Substitution, Shopt lastpipe, Command Execution Environment). Confirmed the subshell cases and the lastpipe condition. Dropped the `cmd & v=1` example line, which did not demonstrate the background case.
