---
id: computing-software.web-development.webassembly.sections-and-indices
name: sections-and-indices
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wasm-sections, function-index-space, custom-sections, wasm-module-sections, wasm-imports-exports, wasm-start-function, wasm]
level: practitioner
status: docs-checked
description: "Module anatomy"
sources: ["https://webassembly.github.io/spec/core/binary/modules.html", "https://webassembly.github.io/spec/core/syntax/modules.html", "https://github.com/WebAssembly/wabt"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sections and index spaces

Goal: understand module layout.
- Sections: type, import, function, table, memory, global, export, start, element, code, data, data count, tag, plus custom (names, producers, source maps).
- Index spaces put imports first, then module definitions.
- Inspect with `wasm-objdump` (WABT).
Verify: you can map a function index to its export name.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: section list including data count and tag; imports precede module definitions in each index space; `wasm-objdump`.
Removed or reworded as unconfirmed: the `-x` flag and `wasm-tools dump` (not on a page read).
Method: documentation only; no commands were run.
