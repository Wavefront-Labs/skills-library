---
id: computing-software.systems-network-administration.bash.test-n-z-operators
name: test-n-z-operators
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, test-n-z-operators, empty-string-test, shell-scripting]
level: intro
status: docs-checked
description: "Test for empty and non-empty strings and unset variables in bash and POSIX sh using -n, -z and parameter expansion."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
  - https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# String emptiness: -n, -z, and unset
**Goal:** check values without surprising false positives.
```bash
[ -z "$v" ] && echo "empty or unset"
[ -n "$v" ] && echo "non-empty"
[[ -v name ]] && echo "set (even if empty)"
[ -n "${v+x}" ] && echo "set"                   # set-ness test via expansion
[ -z "${v-}" ]                                  # safe under set -u
```
- `-z string` is true if the length is zero; `-n string` (or a bare string) is true if the length is non-zero. `-v varname` is true if the variable has been assigned a value.
- Always quote in `[ ]`: `test` decides by argument count, and with one argument the expression is true if that argument is not null, so `[ -n $v ]` with empty `$v` becomes `[ -n ]` and is true.
- The words between `[[` and `]]` do not undergo word splitting or filename expansion, but quoting is still good style.
- `${v:-d}` treats empty like unset; `${v-d}` only unset. `${v+x}` expands to x only when v is set (even if empty).
- `[ "$a" = "$b" ]` uses single `=`: the manual says `=` should be used with `test` for POSIX conformance.
- Self-check: `v=; [ -z "$v" ] && [[ -v v ]] && echo ok`.

## Checked
Method: 2026-11-09 docs-only read of the GNU Bash manual (Bourne Shell Builtins test, Bash Conditional Expressions, Conditional Constructs, Shell Parameter Expansion). Confirmed `-z`, `-n`, `-v`, the one-argument rule, no word splitting in `[[`, `+` and `-` expansions and the `=` note. Removed the bash 4.2 version claim and the POSIX page citation, which were not confirmed.
