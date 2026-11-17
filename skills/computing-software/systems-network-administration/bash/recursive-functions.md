---
id: computing-software.systems-network-administration.bash.recursive-functions
name: recursive-functions
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, recursive-functions, funcnest, shell-scripting]
level: advanced
status: docs-checked
description: "Write recursive bash functions safely with local variables, a FUNCNEST depth limit and result passing via a global variable or stdout."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recursive shell functions
**Goal:** recurse without clobbering state.
```bash
walk() {                       # print a directory tree
  local dir=$1 indent=$2 e
  for e in "$dir"/*; do
    [[ -e $e ]] || continue
    printf '%s%s\n' "$indent" "${e##*/}"
    [[ -d $e ]] && walk "$e" "$indent  "
  done
}
fact() { local n=$1; (( n <= 1 )) && { echo 1; return; }; echo $(( n * $(fact $((n-1))) )); }
```
- Functions may be recursive. Variables are shared between a function and its caller unless declared with `local`, so declare loop and temp variables `local` or recursion overwrites the caller's.
- `$(fact ...)` runs a command substitution per level; to avoid that for deep recursion, pass the result through a global variable instead.
- Bash places no limit on recursion by default. Set `FUNCNEST` to a number greater than 0 (for example `FUNCNEST=100`) and a call that exceeds that nesting level aborts the entire command.
- `local` returns zero unless used outside a function, given an invalid name or a readonly variable, so `local x=$(cmd)` hides cmd's exit status; split declaration and assignment.
- Self-check: `fact 5` prints 120.

## Checked
2026-11-08. Confirmed in the GNU Bash manual: functions may be recursive and bash sets no default limit; FUNCNEST (value greater than 0) aborts the command on exceeding the nesting level; local variables are visible only to the function and what it calls; local's return status rules. Removed: the claim that command substitution "forks per level: slow" (reworded to what the manual supports) and the "(REPLY)" example, which the manual does not suggest for result passing.
Method: documentation only; no commands were run.
