---
id: computing-software.web-development.webassembly.wasm-ld-static-linking
name: wasm-ld-static-linking
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wasm-ld, wasm-object-files, linking-section, dynamic-linking-wasm, side-modules, wasm]
level: practitioner
status: docs-checked
description: "LLVM linker"
sources: ["https://lld.llvm.org/WebAssembly.html", "https://raw.githubusercontent.com/WebAssembly/wabt/main/README.md", "https://raw.githubusercontent.com/WebAssembly/wasi-sdk/main/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static linking with wasm-ld

Goal: link object files.
- Compile objects with clang for a wasm32 target, then `wasm-ld a.o b.o -o out.wasm --export-all --no-entry` (`--export-all` is normally combined with `--no-gc-sections`; `--no-entry` skips the `_start` search).
- Flags: `--import-memory`, `--max-memory`, `--stack-first`, `--allow-undefined`.
- Libraries via `wasi-sdk` sysroot.
Verify: exports listed by `wasm-objdump`.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: `--no-entry`, `--export-all`, `--import-memory`, `--max-memory`, `--stack-first`, `--allow-undefined`, wasi-sysroot.
Removed or reworded as unconfirmed: the exact clang command line and the `-x` flag of `wasm-objdump`.
Method: documentation only; no commands were run.
