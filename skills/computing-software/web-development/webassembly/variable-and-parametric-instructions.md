---
id: computing-software.web-development.webassembly.variable-and-parametric-instructions
name: variable-and-parametric-instructions
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, local-get-set-tee, global-get-set, select-instruction, wasm]
level: practitioner
status: docs-checked
description: "State and stack ops"
sources: ["https://webassembly.github.io/spec/core/syntax/instructions.html", "https://webassembly.github.io/spec/core/valid/instructions.html", "https://webassembly.github.io/spec/core/exec/runtime.html", "https://webassembly.github.io/spec/core/exec/instructions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Locals, globals and parametric instructions

Goal: manipulate state.
- `local.get/set/tee`, `global.get/set` (mutable globals must be declared), `drop`, `select`.
- Locals other than parameters start at their type's default value (0 for number and vector types, null for nullable references).
Verify: a counter global increments across calls.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: `local.get`/`local.set`/`local.tee`, `global.get`/`global.set`, `drop`, `select`; default values.
Removed or reworded as unconfirmed: 'params come first' and the exported mutable globals line.
Method: documentation only; no commands were run.
