---
id: computing-software.systems-network-administration.bash.case-extglob-patterns
name: case-extglob-patterns
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, case-extglob-patterns, extglob-case, shell-scripting]
level: advanced
status: docs-checked
description: "Match with extended globs like @(a|b) and !(x) inside bash case and [[ ]], and enable extglob safely."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# extglob patterns in case
**Goal:** express alternation and negation in case without regex.
```bash
shopt -s extglob                     # enable extended patterns
case $f in
  @(*.jpg|*.png)) echo image ;;
  !(*.tmp))       echo not-tmp ;;
  +([0-9]))       echo digits ;;
esac
[[ $x == ?(pre)name*(.ext) ]]
```
- Forms: `?(p)` 0-1, `*(p)` 0+, `+(p)` 1+, `@(p)` exactly one, `!(p)` anything but.
- Self-check: `shopt -s extglob; case b in @(a|b)) echo y;; esac`.

## Checked

2026-11-02: Confirmed in Pattern Matching (`?(` `*(` `+(` `@(` `!(` forms, require `shopt -s extglob`) and Conditional Constructs (case patterns). Removed: parse-time ordering and `[[ ]]` always-on claims.
Source read: GNU Bash Reference Manual (https://www.gnu.org/software/bash/manual/bash.html).
Method: documentation only; no commands were run.
