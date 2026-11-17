---
id: computing-software.software-engineering.v-lang.v-goto-and-labels
name: v-goto-and-labels
category: computing-software
field: software-engineering
product: v-lang
tags: [v-goto-and-labels, defer-and-goto, goto, unsafe goto, label, jump, low level control flow, v-lang]
level: advanced
status: docs-checked
description: "Use goto with labels in unsafe blocks for rare low-level control flow, with the restrictions and alternatives."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# goto statements

Goal: know goto exists and when to avoid it.

- `goto` jumps unconditionally to a label; the label must be in the same function as the `goto`. The label is written as a statement: `my_label:`.
- A program may `goto` a label outside or deeper than the current scope. Because `goto` can jump past variable initialization or back to code that uses freed memory, it requires `unsafe`: `unsafe { goto my_label }`.
- The docs say `goto` should be avoided, particularly when `for` can be used instead.
- Prefer labelled `break`/`continue` for leaving nested loops; those do not risk violating memory safety.

Verify: refactor a goto-based retry into a `for` with `continue` and compare behaviour.

## Checked

Date: 2026-11-02. Confirmed in the V documentation (doc/docs.md, "Goto" and "Labelled break & continue"). Removed as not stated there: V "positions goto as a last resort" for parsers, label namespace sharing with loop labels, restrictions on jumping over declarations (the docs say it is allowed in `unsafe`), `v translate` goto remarks, the backward-jump termination note.

Method: documentation only; no commands were run.
