---
id: computing-software.systems-network-administration.bash.dparen-arithmetic-test
name: dparen-arithmetic-test
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, dparen-arithmetic-test, double-paren, shell-scripting]
level: practitioner
status: docs-checked
description: "Use (( )) in bash for numeric comparisons, counters and loops instead of -eq inside test brackets."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Arithmetic tests with (( ))
**Goal:** do integer logic readably.
```bash
if (( count > 10 && retries < 3 )); then echo big; fi
(( i++ ))                  # returns 1 (failure) when the result is 0!
(( total += size ))
for (( i=0; i<n; i++ )); do ...; done
x=$(( a * b ))             # arithmetic expansion yields the value
```
- Exit status is 0 if the result is non-zero, 1 if zero. Under `set -e`, `(( i++ ))` from 0 aborts the script: use `i=$((i+1))` or `(( ++i ))` after init.
- Integers only; a constant with a leading 0 is octal, so `08` is invalid.
- Self-check: `(( 0 )); echo $?` prints 1.

## Checked

2026-11-02: Confirmed in Conditional Constructs (`(( expression ))`: status 0 if the value is non-zero, otherwise 1) and Shell Arithmetic (integer evaluation, C operators including ++, += and leading-0 octal), and in Exit-on-error rules of The Set Builtin (a failing compound command triggers errexit). Removed: non-numeric strings evaluate to 0 claim.
Source read: GNU Bash Reference Manual (https://www.gnu.org/software/bash/manual/bash.html).
Method: documentation only; no commands were run.
