---
id: computing-software.systems-network-administration.bash.fd-duplication-swap
name: fd-duplication-swap
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, fd-duplication-swap, fd-swap, shell-scripting]
level: advanced
status: docs-checked
description: "Duplicate, move and swap file descriptors in bash with n>&m, n>&-, exec and temporary fd 3 to split streams."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
  - https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Duplicating and swapping fds
**Goal:** manipulate descriptors beyond 0/1/2.
```bash
cmd 3>&1 1>&2 2>&3 3>&-     # swap stdout and stderr
exec 3>log.txt; echo hi >&3; exec 3>&-   # open, use, close fd 3
out=$(cmd 2>&1 1>/dev/null)  # capture ONLY stderr
exec 4<&0 < input.txt        # save stdin, then redirect
n>&m   # make fd n a copy of m ; n>&- close ; n<>f open read/write
```
- `>&3` duplicates; `>&3-` moves (copies then closes 3).
- Use the `{var}>file` form to have the shell pick a free descriptor of 10 or above: `exec {fd}>f; echo >&$fd`. Hard-coded descriptors above 9 may clash with ones the shell uses.

## Checked

2026-11-02: Confirmed in Redirections (duplicating `n>&m`, closing `n>&-`, moving `n>&digit-`, `n<>word`, `{varname}` allocation of fd >= 10, caution above 9, left-to-right order) and Command Substitution. Removed: inherited-descriptor and /proc claims.
Source read: GNU Bash Reference Manual (https://www.gnu.org/software/bash/manual/bash.html).
Method: documentation only; no commands were run.
