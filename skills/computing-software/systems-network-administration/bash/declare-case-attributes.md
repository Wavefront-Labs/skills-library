---
id: computing-software.systems-network-administration.bash.declare-case-attributes
name: declare-case-attributes
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, declare-case-attributes, declare-upper-lower, shell-scripting]
level: practitioner
status: docs-checked
description: "Force bash variables to upper or lower case on assignment with declare -u and -l, and use -i and -r attributes."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# declare -u and -l case attributes
**Goal:** normalise values automatically.
```bash
declare -u CODE; CODE=abc123; echo "$CODE"     # ABC123
declare -l email; email='Foo@Example.COM'; echo "$email"   # foo@example.com
declare -i n=5; n+=3; echo "$n"                # 8 (arithmetic +=)
declare -r CONST=1                              # read-only
declare -p CODE                                 # shows attributes: declare -u CODE="ABC123"
```
- The conversion happens when the variable is assigned a value.
- Alternative one-off: `${var^^}` and `${var,,}`.
- `declare` inside a function makes the variable local (use `-g` for global).
- Self-check: `declare -p` shows the attribute flags.

## Checked

2026-11-02: Confirmed in Bash Builtins (`declare -u -l -i -r -p -g`: case conversion on assignment, integer arithmetic on assignment, declare in a function makes the name local unless -g) and Shell Parameter Expansion (`^^`, `,,`). Removed: version claim, `+u` behaviour claim.
Source read: GNU Bash Reference Manual (https://www.gnu.org/software/bash/manual/bash.html).
Method: documentation only; no commands were run.
