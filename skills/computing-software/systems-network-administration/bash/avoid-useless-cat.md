---
id: computing-software.systems-network-administration.bash.avoid-useless-cat
name: avoid-useless-cat
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, avoid-useless-cat, useless-cat, shell-scripting]
level: intro
status: docs-checked
description: "Cut forks in shell pipelines by removing useless cat in favour of redirection, tool file arguments and parameter expansion."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
  - https://www.shellcheck.net/wiki/SC2002
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Avoiding useless cat
**Goal:** fewer processes, same result.
```bash
cat file | tr ' ' _ | nl   ->  < file tr ' ' _ | nl
cat file | grep x          ->  grep x file
cat file | while IFS= read -r l; do ...; done   ->  while IFS= read -r l; do ...; done < file
x=$(cat file)              ->  x=$(< file)
```
- ShellCheck SC2002 flags useless cat. It is an optional rule: since ShellCheck 0.11.0 it must be enabled with `enable=useless-use-of-cat` in `.shellcheckrc` (it was not optional before). The wiki says removing cat from a short-lived pipeline in a loop can speed it up by 2x, but that it rarely affects correctness: ignore as you see fit.
- Redirection also helps programs that benefit from seekable input, such as `tail` or `tar`.
- Bash runs each command of a multi-command pipeline in its own subshell, so `cat file | while read ...` runs the loop in a subshell and variables set in it are lost; `while ... done < file` keeps the loop in the current shell. (The `lastpipe` option can run the last pipeline element in the current shell when job control is not active.)
- The bash manual says `$(cat file)` can be replaced by the equivalent but faster `$(< file)`.
- Other forks to drop: `${x^^}` uppercases a variable's value (`${parameter^^pattern}`), and `${f##*/}` strips the longest leading match (`${parameter##word}`).
- Exception: `cat` is still right for concatenating files (or stdin plus files).
- Self-check: the pipeline output is unchanged after the rewrite.

## Checked
2026-11-09. Confirmed in the SC2002 wiki page (optional rule, 0.11.0 note, 2x remark, redirection and file-argument advice) and the bash manual (pipeline subshells and lastpipe, `$(< file)`, `${parameter^^pattern}`, `${parameter##word}`). Removed: `ls | grep` glob replacement, `grep -c`, `wc -l <`, `basename` replacement, and the `strace -c` self-check, none of which the cited pages state.
Method: documentation only; no commands were run.
