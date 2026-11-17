---
id: computing-software.systems-network-administration.bash.base-n-constants
name: base-n-constants
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, base-n-constants, octal-leading-zero, shell-scripting]
level: advanced
status: docs-checked
description: "Use bash base#number notation and avoid leading-zero octal errors like 08 and 09."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Numeric bases and octal traps
**Goal:** read and convert numbers in other bases.
```bash
echo $(( 2#1010 ))   # 10
echo $(( 16#ff ))    # 255 ; also 0xff
echo $(( 010 ))      # 8  (leading zero = octal)
n=08; echo $(( 10#$n ))        # force decimal: 8
```
- `$(( 08 ))` is an error: a leading 0 means octal and 8 is not an octal digit.
- `base#` supports bases 2 to 64.
- Self-check: `m=09; echo $((10#$m + 1))` prints 10.

## Checked

2026-11-02: Confirmed in Shell Arithmetic (constants: leading 0 octal, 0x hex, `[base#]n` with base 2 to 64). Removed: printf conversions, the exact error text, `date +%m` and 10#var edge claims.
Source read: GNU Bash Reference Manual (https://www.gnu.org/software/bash/manual/bash.html).
Method: documentation only; no commands were run.
