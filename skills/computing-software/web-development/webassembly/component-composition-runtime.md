---
id: computing-software.web-development.webassembly.component-composition-runtime
name: component-composition-runtime
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wasm-tools-component, wac-compose, wasmtime-component, wasm]
level: practitioner
status: docs-checked
description: "Composition"
sources: ["https://raw.githubusercontent.com/bytecodealliance/wasm-tools/main/README.md", "https://component-model.bytecodealliance.org/composing-and-distributing/composing.html", "https://component-model.bytecodealliance.org/running-components/wasmtime.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Composing and running components

Goal: link components.
- Convert a core module with adapters (`wasm-tools component new my-core.wasm -o my-component.wasm --adapt wasi_snapshot_preview1.reactor.wasm`).
- Compose components to satisfy imports; run with `wasmtime run`.
- Composition cares about interface versions; `wasm-tools component wit` shows a component's embedded imports and exports.
Verify: composed component runs end to end.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: `component new --adapt` with the reactor adapter, `component wit`, composing and `wasmtime run` pages.
Removed or reworded as unconfirmed: the adapter file name `wasi_snapshot_preview1.wasm` (docs show `.reactor.wasm`) and the 'confirm versions' hedge.
Method: documentation only; no commands were run.
