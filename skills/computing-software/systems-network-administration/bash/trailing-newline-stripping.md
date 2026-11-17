---
id: computing-software.systems-network-administration.bash.trailing-newline-stripping
name: trailing-newline-stripping
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, trailing-newline-stripping, strip-trailing-newlines, shell-scripting]
level: practitioner
status: docs-checked
description: "Handle command substitution removing trailing newlines in bash, preserving them when needed with a sentinel."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Trailing newlines in $(...)
**Goal:** know what `$(cmd)` drops.
```bash
x=$(printf 'a\n\n\n'); [[ $x == a ]]       # all trailing newlines removed
x=$(cat file; echo .); x=${x%.}            # keep exact content via sentinel
y=$(<file)                                  # bash shortcut for $(cat file)
```
- Command substitution replaces itself with the command's standard output with any trailing newlines deleted. Embedded newlines are not deleted, but they may be removed during word splitting.
- The manual says `$(cat file)` can be replaced by the equivalent but faster `$(< file)`.
- To keep trailing newlines append a sentinel character inside the substitution, then strip it with `${x%.}`. The brace form `${| command; }` instead expands to the value of `REPLY` without removing trailing newlines.
- Unquoted `$x` later undergoes word splitting; quote it.
- For multi-line file content into an array use `mapfile -t arr < file` instead.
- Self-check: `x=$(printf 'a\n\n'); printf '%s' "$x" | wc -c` prints 1.

## Checked
Method: 2026-11-09 docs-only read of the GNU Bash manual (Command Substitution, Mapfile). Confirmed trailing-newline deletion, embedded newlines, `$(< file)` equivalence and the `${| ...; }` form. Removed the NUL-byte warning claim and the POSIX page citation, which were not confirmed.
