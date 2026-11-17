---
id: computing-software.web-development.webassembly.wabt-and-wasm-tools
name: wabt-and-wasm-tools
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wasm2wat, wasm-objdump, wasm-tools-print, wasm]
level: practitioner
status: docs-checked
description: "Inspecting binaries"
sources: ["https://raw.githubusercontent.com/WebAssembly/wabt/main/README.md", "https://raw.githubusercontent.com/bytecodealliance/wasm-tools/main/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WABT and wasm-tools

Goal: inspect and convert.
- WABT: `wasm2wat`, `wat2wasm`, `wasm-objdump`, `wasm-validate`, `wasm-strip`, `wasm2c`; Bytecode Alliance `wasm-tools`: `parse` (text to binary), `print` (binary to text), `component new`.
- Use name sections for readable traces.
Verify: round trip wat -> wasm -> wat is stable.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: WABT tool list and the `wasm-tools parse`, `print` and `component new` subcommands.
Removed or reworded as unconfirmed: the `-d` flag of `wasm-objdump` and `wasm-decompile`.
Method: documentation only; no commands were run.
