---
id: computing-software.systems-network-administration.bash.nested-command-substitution
name: nested-command-substitution
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, nested-command-substitution, dollar-paren-nesting, shell-scripting]
level: practitioner
status: docs-checked
description: "Nest command substitution with $(...) instead of backticks, with correct quoting at each level."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
  - https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nesting $(...)
**Goal:** compose substitutions without escaping hell.
```bash
msg=$(echo "$(echo inner) outer")           # quotes nest freely inside $(...)
old=`echo \`echo inner\` outer`             # backticks need escapes: avoid
```
- Inside `$( )` quoting is a fresh context: wrap each inner substitution in its own double quotes.
- `$(cmd)` runs in a subshell; variable assignments inside are lost.
- Self-check: `[ "$(echo "$(echo hi there)")" = "hi there" ]`.

## Checked

2026-11-02: Confirmed in Command Substitution (`$(command)` form, backquote form deprecated, run in a subshell environment) and Quoting. Removed: external-command examples (dirname/readlink/grep/find/cut), ShellCheck SC2006, inner-failure claim, backtick escape rules not read.
Source read: GNU Bash Reference Manual (https://www.gnu.org/software/bash/manual/bash.html).
Method: documentation only; no commands were run.
