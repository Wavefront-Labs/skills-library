---
id: computing-software.systems-network-administration.bash.read-timeout-prompt
name: read-timeout-prompt
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, read-timeout-prompt, read-t-timeout, shell-scripting]
level: practitioner
status: docs-checked
description: "Prompt with a timeout in bash using read -t, -p, -n and default answers, and distinguish timeout from EOF."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# read with -t timeout and -p prompt
**Goal:** interactive input that cannot hang forever.
```bash
if read -r -t 10 -p "Continue? [y/N] " ans; then :; else
  rc=$?; (( rc > 128 )) && echo "timed out"; ans=N
fi
read -r -n1 -p "Press key" k        # single character, no Enter
read -r -e -i "$default" -p "Name: " name   # readline editing with prefilled text
[[ ${ans,,} == y* ]] && go
```
- `-t timeout`: timeout may be fractional; on timeout read returns a status greater than 128 and saves any partial input in the variable. The exit status is also non-zero at end-of-file, so test for above 128 to tell a timeout from EOF.
- `-t` only has effect when reading from a terminal, pipe or other special file, not a regular file.
- `-p prompt` is displayed (no trailing newline) only if input comes from a terminal.
- `-n nchars` returns after nchars characters without waiting for Enter, but still honours a delimiter read earlier; `-N nchars` ignores delimiters and reads exactly nchars.
- `-e` uses Readline when stdin is a terminal and `-i text` pre-fills the editing buffer (only when Readline is used).
- `-t 0` returns immediately without reading: status 0 if input is available (or EOF would be returned), non-zero otherwise.
- If TMOUT is set above zero, read uses it as its default timeout.
- Guard non-interactive runs: `[[ -t 0 ]] || { echo "need a tty" >&2; exit 1; }`.
- Self-check: `read -t 1 x; echo $?` at a terminal with no input prints a number above 128.

## Checked
2026-11-08: confirmed against the GNU Bash Reference Manual (single-page bash.html): the read builtin options -e, -i, -n, -N, -p, -r, -s, -t and its exit-status paragraph, and the TMOUT variable. Removed the claim that status 1 means EOF (the manual says only non-zero) and the `-t 0` wording was corrected to match. The `-t fd` conditional (true when fd refers to a terminal) was confirmed in Bash Conditional Expressions.
Method: documentation only; no commands were run.
