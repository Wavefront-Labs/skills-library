---
id: computing-software.systems-network-administration.bash.posix-no-arrays
name: posix-no-arrays
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, posix-no-arrays, positional-list, shell-scripting]
level: advanced
status: docs-checked
description: "Replace bash arrays in POSIX sh using set -- positional lists, newline-delimited strings and careful quoting."
sources:
  - https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Arrays without arrays in POSIX sh
**Goal:** hold a list in a POSIX shell that has no array variables.
```sh
set -- one "two words" three         # positional parameters hold the list
for item in "$@"; do printf '%s\n' "$item"; done
set -- "$@" four                      # append
n=$#; first=$1
shift                                 # remove first
list=$(printf '%s\n' a b c)           # newline-delimited: only for items without newlines
IFS='
'; set -f; for x in $list; do printf '%s\n' "$x"; done; set +f
```
- `set -- args...` unsets all positional parameters, then assigns the arguments in order and sets `#`. `set --` with no arguments unsets them all and sets `#` to zero. The `--` stops a first argument starting with `+` or `-` being read as an option.
- `shift [n]` moves parameter 1+n into 1, and so on, and updates `#`.
- `"$@"` produces one field per positional parameter (and zero fields when there are none), so it passes a list to a command with each element intact. `"$*"` joins them into one field using the first character of `IFS`.
- A function call temporarily replaces the positional parameters and `#` with its operands, and when the function completes they are restored; `set --` inside a function therefore changes only that call's list.
- Unquoted `$list` is subject to field splitting on `IFS` and then pathname expansion; `set -f` disables pathname expansion and `set +f` turns it back on. Setting `IFS` to a newline splits only at newlines.
- The spec describes array assignment only as an "extended assignment syntax" some shells support (in its export and readonly notes), not as a standard feature.

## Checked
Date: 2026-11-07
Method: Read POSIX Shell Command Language (V3_chap02) sections on special parameters `@` and `*`, IFS, field splitting, Function Definition Command, and the set and shift utility entries (set --, -f, +f, shift [n]). Searched the long page for these entries rather than reading every section. Trims: removed the unsourced claims about dash/busybox, "no associative arrays: use case or files/awk", "change the shebang to bash", the `checkbashisms` self-check, and "never build commands by string concatenation" (reworded to the documented `"$@"` field behaviour).
