---
id: computing-software.software-engineering.nim.block-break-continue
name: block-break-continue
category: computing-software
field: software-engineering
product: nim
tags: [block-break-continue, control-flow, block, break, continue, label, nested-loop, return, nim]
level: practitioner
status: docs-checked
description: "Use Nim block labels, break out of nested loops, continue, and block expressions."
sources:
  - https://nim-lang.org/docs/manual.html
  - https://nim-lang.org/docs/tut1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Named blocks, break and continue

Goal: exit nested control flow cleanly.

- `block outer:` opens a named scope; `break outer` leaves that block from inside nested loops.
- `while` and `for` open an implicit block, so `break` can leave them. Identifiers are visible only in the block that declares them, and an explicit `block` opens a new one.
- `break` can leave a `while`, a `for` or a `block`. It leaves the innermost construct unless the label of an enclosing block is given.
- A block expression is like a block statement but yields the last expression under the block as its value.
- `continue` starts the next iteration of the surrounding loop and is only allowed within a loop.

Verify: a search through a 2D seq stops at the first match using `break outer`.

## Checked

2026-11-08. Searched the Nim manual (Block statement, Break statement, While statement, Continue statement, block expression, For statement) and the tutorial (Scopes and the block statement, Break statement, Continue statement). The bullets above match those sections.

Removed as unconfirmed: the `break` inside `case` note, the claim that labels share the identifier namespace, the advice about `return` and a `found` flag, and the lib index source (not used).

Method: documentation only; no commands were run.
