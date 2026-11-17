---
id: computing-software.web-development.webassembly.custom-sections-name-section
name: custom-sections-name-section
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, name-section, producers-section, source-mapping-url, wasm]
level: practitioner
status: docs-checked
description: "Metadata"
sources: ["https://webassembly.github.io/spec/core/binary/modules.html", "https://webassembly.github.io/spec/core/appendix/custom.html", "https://github.com/WebAssembly/wabt"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom sections and the name section

Goal: use metadata sections.
- The name section is a custom section giving names to functions and locals for debugging.
- Strip for release with `wasm-strip` (WABT removes sections from a binary), keep for profiling.
- Custom sections have id 0 and are ignored by the WebAssembly semantics.
Verify: stack traces show names when the section is kept.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: custom section id 0 and that the semantics ignore them; the name section; `wasm-strip` removes sections.
Removed or reworded as unconfirmed: `producers`, `sourceMappingURL` and `wasm-opt --strip-debug` (not on a page read).
Method: documentation only; no commands were run.
