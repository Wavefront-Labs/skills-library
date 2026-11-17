---
id: computing-software.web-development.webassembly.rust-wasm-size-and-perf
name: rust-wasm-size-and-perf
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wasm-opt-rust, twiggy, wee-alloc, wasm]
level: practitioner
status: docs-checked
description: "Smaller binaries"
sources: ["https://raw.githubusercontent.com/rustwasm/book/master/src/reference/code-size.md", "https://raw.githubusercontent.com/rustwasm/twiggy/master/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Size and performance tuning in Rust Wasm

Goal: reduce size.
- `twiggy top -n 20 file.wasm` shows size contributors.
- Panics already translate to aborts on `wasm32-unknown-unknown`; slice indexing, division and unwrapping are common hidden panic sources.
- The default allocator is a dlmalloc port; the book describes `wee_alloc` as a smaller, slower alternative.
Verify: size drops measurably after each change.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: `twiggy top`, panic sources, dlmalloc and `wee_alloc`.
Removed or reworded as unconfirmed: `panic = "abort"`, `codegen-units = 1` and the formatting-machinery claim.
Method: documentation only; no commands were run.
