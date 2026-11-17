---
id: computing-software.web-development.webassembly.active-vs-passive-segments
name: active-vs-passive-segments
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, data-segment, elem-segment, table-init, wasm-globals, element-segments, active-passive-segments, wasm]
level: practitioner
status: docs-checked
description: "Initialisation"
sources: ["https://webassembly.github.io/spec/core/syntax/modules.html", "https://webassembly.github.io/spec/core/valid/modules.html", "https://webassembly.github.io/spec/core/exec/modules.html", "https://webassembly.github.io/spec/core/exec/instructions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Active, passive and declarative segments

Goal: initialise memory and tables.
- Active segments copy at instantiation to an offset; passive segments are copied on demand via `memory.init`/`table.init`; declarative element segments are not available at runtime and only forward-declare references formed by `ref.func`.
- Offsets are constant expressions, which can read imported or previously defined globals.
- Active segments are applied during instantiation by running `memory.init`/`table.init` followed by a drop, so an out-of-range offset traps and instantiation fails.
Verify: instantiation fails cleanly when the offset is too large.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: active, passive and declarative modes; `memory.init`/`table.init`; constant-expression offsets and global access; instantiation running init plus drop.
Removed or reworded as unconfirmed: the claim that offsets are specifically `global.get` of an imported global.
Method: documentation only; no commands were run.
