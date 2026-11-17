---
id: computing-software.systems-network-administration.bash.command-builtin-bypass
name: command-builtin-bypass
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, command-builtin-bypass, shell-scripting]
level: advanced
status: docs-checked
description: "Wrap a builtin or external command in a bash function and call the original with command or builtin."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
  - https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wrapping builtins: command and builtin
**Goal:** override `cd`, `ls` etc. without infinite recursion.
```bash
cd() { builtin cd "$@" && pwd; }         # builtin: skip functions/aliases
pwd() { command pwd -P; }               # command: skip functions
type -a cd                               # show all definitions in order
unset -f cd pwd; unalias cd 2>/dev/null   # remove overrides
\cd                                      # quoting part of the word stops alias expansion
```
- `builtin` only works for builtins; `command` works for both.
- Overriding `cd` in scripts surprises later code: keep overrides in interactive rc files.
- Self-check: after defining the wrapper, `type cd` says function and `builtin type cd` says builtin.

## Checked

2026-11-02: Confirmed in Bourne Shell Builtins / Bash Builtins (`builtin`, `command`, `type -a`, `unalias`, `unset -f`) and Aliases (quoting a word prevents alias expansion). Removed: command -v/-p claims.
Source read: GNU Bash Reference Manual (https://www.gnu.org/software/bash/manual/bash.html).
Method: documentation only; no commands were run.
