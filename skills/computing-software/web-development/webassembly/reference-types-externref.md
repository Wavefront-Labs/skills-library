---
id: computing-software.web-development.webassembly.reference-types-externref
name: reference-types-externref
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, externref, funcref, table-get-set, wasm]
level: practitioner
status: docs-checked
description: "Host objects"
sources: ["https://webassembly.github.io/spec/core/syntax/types.html", "https://webassembly.github.io/spec/core/syntax/instructions.html", "https://webassembly.github.io/spec/core/exec/instructions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reference types and externref

Goal: pass host objects.
- `externref` references are opaque to Wasm: neither their size nor bit pattern is observable.
- Tables can hold references, so a table of `externref` can serve as a handle table.
- Typed references and GC types (`struct.new`, `array.fill`) are part of the current core spec.
Verify: a host object round-trips through Wasm unchanged.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: opaque references; tables of references; GC instructions in the core spec.
Removed or reworded as unconfirmed: the JS API claim that JS values pass directly.
Method: documentation only; no commands were run.
