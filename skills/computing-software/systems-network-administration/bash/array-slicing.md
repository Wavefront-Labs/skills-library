---
id: computing-software.systems-network-administration.bash.array-slicing
name: array-slicing
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, array-slicing, array-append, shell-scripting]
level: practitioner
status: docs-checked
description: "Slice, append to, copy and delete elements from bash indexed arrays with ${arr[@]:off:len} and +=."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Array slicing and appending
**Goal:** manipulate arrays without loops.
```bash
a=(a b c d e)
echo "${a[@]:1:3}"       # b c d
echo "${a[@]: -2}"       # d e  (space before minus)
a+=(f g)                 # append
b=("${a[@]}")            # copy (quote it!)
unset 'a[1]'             # leaves a hole; indices not renumbered
a=("${a[@]}")            # re-pack indices
echo "${a[-1]}"          # last element (negative subscripts count from the end)
```
- `"${a[*]}"` joins with the first char of IFS.
- Positional params slice similarly: `"${@:2}"`.
- Self-check: `a=(1 2 3); a+=(4); echo "${#a[@]} ${a[@]:2}"` prints `4 3 4`.

## Checked

2026-11-02: Confirmed in Arrays, Shell Parameter Expansion (substring expansion, negative offset needs a space), Special Parameters (`"${a[*]}"` joins with first IFS character): slicing, `+=` append, `unset a[i]`, negative subscripts. Removed: bash 4.3 version tag, unquoted-loses-empty-elements, sparse-offset claim.
Source read: GNU Bash Reference Manual (https://www.gnu.org/software/bash/manual/bash.html).
Method: documentation only; no commands were run.
