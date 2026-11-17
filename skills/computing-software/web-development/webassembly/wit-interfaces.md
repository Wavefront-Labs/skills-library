---
id: computing-software.web-development.webassembly.wit-interfaces
name: wit-interfaces
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wit-world, wit-interface, wit-bindgen, component-model, wit, wasm-components, wasm]
level: practitioner
status: docs-checked
description: "Typed interfaces"
sources: ["https://component-model.bytecodealliance.org/design/wit.html", "https://component-model.bytecodealliance.org/design/worlds.html", "https://raw.githubusercontent.com/bytecodealliance/wit-bindgen/main/README.md", "https://raw.githubusercontent.com/bytecodealliance/wac/main/README.md", "https://raw.githubusercontent.com/WebAssembly/wasi-http/main/wit/proxy.wit"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WIT interface definitions

Goal: define component interfaces.
- WIT describes interfaces, worlds, records, variants, resources; `wit-bindgen` generates guest bindings for Rust, C, C++, C# and Go.
- Compose with `wasm-tools component new`, `wac plug`.
- Preview 2 worlds: `wasi:cli/command`, `wasi:http/proxy`.
Verify: component builds and its WIT validates.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: WIT concepts, `wit-bindgen` languages, `wasm-tools component new`, `wac plug`, `wasi:cli/command`, `wasi:http/proxy`.
Removed or reworded as unconfirmed: the `wit-bindgen rust|c|go` command form.
Method: documentation only; no commands were run.
