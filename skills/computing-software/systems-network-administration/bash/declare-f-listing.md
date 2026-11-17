---
id: computing-software.systems-network-administration.bash.declare-f-listing
name: declare-f-listing
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, declare-f-listing, declare-f, export-function, shell-scripting]
level: practitioner
status: docs-checked
description: "List, print and export function definitions in bash with declare -f, declare -F, type and export -f."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Listing functions with declare -f
**Goal:** inspect and reuse functions.
```bash
declare -F                 # names only
declare -f myfunc          # full definition (reusable source)
type myfunc                # also shows what kind of command
declare -f myfunc > lib.sh # save for sourcing
export -f myfunc           # visible to child bash processes
```

## Checked

2026-11-02: Confirmed in Bash Builtins (`declare -f`, `-F` prints only names and attributes, `-F` implies `-f`; `type`) and Shell Functions / Bourne Shell Builtins (`export -f` exports functions to children through the environment). Removed: BASH_FUNC encoding, xargs/find, formatting and exit-status claims.
Source read: GNU Bash Reference Manual (https://www.gnu.org/software/bash/manual/bash.html).
Method: documentation only; no commands were run.
