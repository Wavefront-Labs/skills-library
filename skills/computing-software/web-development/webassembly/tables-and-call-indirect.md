---
id: computing-software.web-development.webassembly.tables-and-call-indirect
name: tables-and-call-indirect
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, call-indirect, funcref-table, indirect-function-calls, wasm-table, externref, wasm]
level: practitioner
status: docs-checked
description: "Function pointers"
sources: ["https://developer.mozilla.org/en-US/docs/WebAssembly/Guides/Understanding_the_text_format", "https://webassembly.github.io/spec/core/exec/instructions.html", "https://webassembly.github.io/spec/core/syntax/instructions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tables and call_indirect

Goal: implement function pointers.
- Tables hold function references, so compilers use table indices as function pointers; `call_indirect (type $sig)` checks the signature at runtime.
- Tables grow with `table.grow`; element segments initialise them.
Verify: calling the wrong signature traps.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: `call_indirect (type $sig)` text syntax; the instruction is `table.get`, `ref.cast` to the type, then `call_ref`; `table.grow` returns the old size or -1.
Removed or reworded as unconfirmed: the dynamic-linking sentence.
Method: documentation only; no commands were run.
