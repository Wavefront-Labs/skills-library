---
id: computing-software.systems-network-administration.bash.line-continuation
name: line-continuation
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, line-continuation, shell-scripting]
level: intro
status: docs-checked
description: "Continue long bash commands across lines with backslash, pipes and operators, and avoid trailing-space and comment breakage."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Line continuation
**Goal:** keep long commands readable without breaking them.
```bash
printf '%s\n' one \
      two \
      three
```
- The backslash must be the LAST character: a trailing space turns it into an escaped space and the next line runs as its own command.
- Inside double quotes a backslash-newline is removed; inside single quotes it is kept literally.

## Checked

2026-11-02: Confirmed in Quoting (an unquoted backslash before a newline is removed as line continuation; within double quotes backslash-newline is removed; single quotes keep it) and Shell Syntax. Removed: trailing-pipe/&& continuation examples, comment placement claim, ShellCheck SC1101, rsync/grep/sort examples.
Source read: GNU Bash Reference Manual (https://www.gnu.org/software/bash/manual/bash.html).
Method: documentation only; no commands were run.
