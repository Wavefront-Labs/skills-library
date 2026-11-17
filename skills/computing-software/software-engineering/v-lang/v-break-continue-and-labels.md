---
id: computing-software.software-engineering.v-lang.v-break-continue-and-labels
name: v-break-continue-and-labels
category: computing-software
field: software-engineering
product: v-lang
tags: [v-break-continue-and-labels, loops-and-labels, break, continue, label, labeled loop, nested loops, outer loop, v-lang]
level: practitioner
status: docs-checked
description: "Exit or skip iterations, and break or continue an outer loop using labels placed before the for statement."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# break, continue and labeled loops

Goal: control nested loops.

- `break` and `continue` control the innermost `for` loop by default.
- Followed by a label name they refer to an outer `for` loop: `outer: for i := 4; true; i++ { for { if i < 7 { continue outer } else { break outer } } }` (prints 4 to 7).
- The label must immediately precede the outer loop. A labelled loop can iterate over a `filter` or `map` result.
- `goto` is the unsafe alternative; labelled `break`/`continue` do not risk violating memory safety.

Verify: search a 2D grid for the first match and stop both loops.

## Checked

Date: 2026-11-02. Confirmed in the V documentation (doc/docs.md, "Labelled break & continue", "Goto"). Removed as not stated there: behaviour of `break` inside `match`, `break`/`continue` inside `or {}` blocks, label naming rules, "labelled blocks are not supported", label reuse rule.

Method: documentation only; no commands were run.
