---
id: computing-software.systems-network-administration.bash.associative-array-keys
name: associative-array-keys
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, associative-array-keys, hash-map, shell-scripting]
level: practitioner
status: docs-checked
description: "Create bash 4 associative arrays, iterate keys and values, test membership and delete keys."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Associative array keys and iteration
**Goal:** use maps in bash.
```bash
declare -A age=([alice]=30 [bob]=25)
age[carol]=41
for k in "${!age[@]}"; do echo "$k=${age[$k]}"; done
[[ -v age[bob] ]] && echo present          # key exists
[[ ${age[x]+set} ]] || echo missing        # portable membership test
unset 'age[bob]'
echo "${#age[@]}"                           # entries
```
- `declare -A` is mandatory; without it the keys are evaluated as arithmetic and every key is evaluated as an arithmetic expression instead of used as a string.
- Keys with spaces need quotes: `age["a b"]=1`.
- Self-check: `declare -A m; m[a]=1; [[ -v m[a] ]] && echo ok`.

## Checked

2026-11-02: Confirmed in Arrays (`declare -A`, indexed subscripts are arithmetic), Shell Parameter Expansion (`${!name[@]}`, `${#name[@]}`, `${parameter+word}`), Bash Conditional Expressions (`-v name[key]`). Removed: version claims, macOS, iteration-order, export claims.
Source read: GNU Bash Reference Manual (https://www.gnu.org/software/bash/manual/bash.html).
Method: documentation only; no commands were run.
