---
id: computing-software.systems-network-administration.bash.parameter-length
name: parameter-length
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, parameter-length, string-length, shell-scripting]
level: intro
status: docs-checked
description: "Get string length and array element counts in bash with ${#var}, ${#arr[@]} and the multibyte caveat."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Length expansion ${#var}
**Goal:** count characters, elements and arguments.
```bash
s="héllo"; echo "${#s}"            # characters (locale-aware): 5
LC_ALL=C; echo "${#s}"             # counts in the C locale: 6 if the source is UTF-8
arr=(a b c); echo "${#arr[@]}"     # 3 elements
echo "${#arr[1]}"                  # length of element 1
echo "$#"                          # number of positional args
declare -A m=([k]=v); echo "${#m[@]}"
```
- `${#arr}` is the length of element 0, not the count: use `${#arr[@]}`.
- Self-check: `a=(x y z); unset 'a[1]'; echo "${#a[@]}"` prints 2.

## Checked

2026-11-02: Confirmed in Shell Parameter Expansion (`${#parameter}` length in characters, `${#name[subscript]}`, `[@]` gives the element count, `${#arr}` is element 0) and Bash Variables (LC_CTYPE governs character interpretation). Removed: sparse-array and bytes-versus-characters claims.
Source read: GNU Bash Reference Manual (https://www.gnu.org/software/bash/manual/bash.html).
Method: documentation only; no commands were run.
