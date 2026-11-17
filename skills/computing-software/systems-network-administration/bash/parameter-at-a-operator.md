---
id: computing-software.systems-network-administration.bash.parameter-at-a-operator
name: parameter-at-a-operator
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, parameter-at-a-operator, at-a-operator, shell-scripting]
level: advanced
status: docs-checked
description: "Use bash 4.4 parameter transformation operators ${var@a}, @A, @Q, @E, @P to read attributes and re-quote values."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The @a and @A transformations
**Goal:** introspect variables compactly.
```bash
declare -ir n=5
echo "${n@a}"            # attribute flags: ir
echo "${n@A}"            # declare -ir n='5'  (re-creatable assignment)
x='a b'; echo "${x@Q}"   # 'a b'  quoted for reuse
y='tab\there'; echo "${y@E}"   # expand backslash escapes
echo "${PS1@P}"          # expand prompt escapes
arr=(x y); echo "${arr@A}"
```
- Transformations: `@Q` quote, `@E` escapes, `@P` prompt, `@A` assignment form, `@a` attributes, `@U/@L/@u` case conversion.

## Checked

2026-11-02: Confirmed in Shell Parameter Expansion (`${parameter@operator}`: U, u, L, Q, E, P, A, a operators and their meanings). Removed: version claims, dash claim, logging-safety claim.
Source read: GNU Bash Reference Manual (https://www.gnu.org/software/bash/manual/bash.html).
Method: documentation only; no commands were run.
