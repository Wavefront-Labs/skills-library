---
id: computing-software.systems-network-administration.bash.command-grouping
name: command-grouping
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, command-grouping, brace-group, shell-scripting]
level: practitioner
status: docs-checked
description: "Choose between brace groups { ...; } and subshell parentheses (...) for redirecting, scoping and isolating commands."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
  - https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Brace group vs subshell
**Goal:** group commands with the right scope.
```bash
{ echo header; sort data; } > out.txt     # one redirection, same shell
( cd "$dir" && make )                      # cwd and vars isolated
{ read -r a; read -r b; } < file          # share one stdin
cmd || { echo "failed" >&2; exit 1; }      # multi-command handler
```
- Braces need a space after `{` and a `;` or newline before `}`.
- `( )` forks a subshell: variable assignments, `cd`, `set`, `exit` do not escape it.
- `exit` inside `( )` leaves only the subshell; inside `{ }` it exits the script.
- A pipeline stage also runs in a subshell: `{ x=1; } | cat` loses `x`.
- Self-check: `(x=1); echo "${x-unset}"` prints unset; `{ x=1; }; echo $x` prints 1.

## Checked

2026-11-02: Confirmed in Command Grouping (`( list )` forks a subshell and assignments do not persist; `{ list; }` runs in the current shell, semicolon or newline required, braces are reserved words), Pipelines (each multi-command pipeline element runs in its own subshell) and Compound Commands.
Source read: GNU Bash Reference Manual (https://www.gnu.org/software/bash/manual/bash.html).
Method: documentation only; no commands were run.
