---
id: computing-software.web-development.webassembly.function-and-block-types
name: function-and-block-types
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wasm-functype, multi-value, block-types, wasm]
level: practitioner
status: docs-checked
description: "Signatures"
sources: ["https://webassembly.github.io/spec/core/syntax/types.html", "https://webassembly.github.io/spec/core/syntax/instructions.html", "https://github.com/WebAssembly/wabt"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Function types and block types

Goal: read and write function signatures.
- A function type maps parameter types to result types; multi-value allows several results.
- A block type is an optional value type or a type index (the type index form carries multiple parameters and results).
- Imports and exports are typed by these signatures.
Verify: `wasm-validate` accepts the module and signatures match imports.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: function types as parameter and result lists; block type grammar (optional value type or type index); `wasm-validate`.
Removed or reworded as unconfirmed: the word 'empty' as a separate form (it is the absent optional value type).
Method: documentation only; no commands were run.
