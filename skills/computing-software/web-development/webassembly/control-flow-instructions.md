---
id: computing-software.web-development.webassembly.control-flow-instructions
name: control-flow-instructions
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wasm-block-loop-br, br-table, structured-control-flow, wasm]
level: practitioner
status: docs-checked
description: "Structured control"
sources: ["https://webassembly.github.io/spec/core/syntax/instructions.html", "https://webassembly.github.io/spec/core/exec/instructions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Control flow: block, loop, br

Goal: write loops and branches.
- `block` / `loop` / `if` define labels; `br N` branches outward by depth N (loop label branches to the start, block label to the end).
- `br_table` implements switch; `br_if` conditional.
- Control flow is structured; label indices are relative to the enclosing blocks.
Verify: a counting loop terminates with the expected sum.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: `block`/`loop`/`if` labels, relative label indices, backward jump to the start of a `loop` and the end continuation of a `block`, `br_if`, `br_table`.
Removed or reworded as unconfirmed: the 'no arbitrary goto' wording.
Method: documentation only; no commands were run.
