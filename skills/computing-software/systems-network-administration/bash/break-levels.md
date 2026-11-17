---
id: computing-software.systems-network-administration.bash.break-levels
name: break-levels
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, break-levels, shell-scripting]
level: practitioner
status: docs-checked
description: "Leave nested bash loops with break N and continue N, and refactor deep nesting into functions."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
  - https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# break N and continue N
**Goal:** exit or skip several loop levels at once.
```bash
for host in "${hosts[@]}"; do
  for port in 22 443; do
    if probe "$host" "$port"; then found=$host; break 2; fi   # exit both loops
  done
done
while read -r l; do
  [[ $l == \#* ]] && continue      # skip comment lines
done < file
```
- `break 2` leaves two enclosing loops; N must be 1 or greater.
- `continue 2` resumes the next iteration of the outer loop.
- Cleaner for deep nests: put the loops in a function and use `return`.
- Self-check: a 2x2 loop that echoes then `break 2` on the first item prints once.

## Checked

2026-11-02: Confirmed in Bourne Shell Builtins (`break [n]`, `continue [n]`: nth enclosing for, while, until or select loop, n >= 1). Removed: over-large N behaviour, behaviour outside loops and in functions.
Source read: GNU Bash Reference Manual (https://www.gnu.org/software/bash/manual/bash.html).
Method: documentation only; no commands were run.
