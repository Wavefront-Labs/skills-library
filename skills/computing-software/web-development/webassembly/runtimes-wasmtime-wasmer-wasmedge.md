---
id: computing-software.web-development.webassembly.runtimes-wasmtime-wasmer-wasmedge
name: runtimes-wasmtime-wasmer-wasmedge
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wasmtime-embed, wasmer-run, wasmedge, wasm]
level: practitioner
status: docs-checked
description: "Runtimes"
sources: ["https://docs.wasmtime.dev/api/wasmtime/struct.Config.html", "https://raw.githubusercontent.com/wasmerio/wasmer/main/README.md", "https://raw.githubusercontent.com/WasmEdge/WasmEdge/master/README.md", "https://raw.githubusercontent.com/tetratelabs/wazero/main/README.md", "https://raw.githubusercontent.com/wasm3/wasm3/main/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Runtime selection and embedding

Goal: pick and embed a runtime.
- Wasmtime (Bytecode Alliance), Wasmer, WasmEdge, wazero (Go), wasm3 (interpreter).
- Wasmtime `Config::consume_fuel` and `Config::epoch_interruption` bound execution; when fuel runs out a trap is raised, and a `Store` starts with no fuel, so add fuel before running.
- wazero is a zero-dependency runtime for Go; the Wasmer SDK embeds Wasmer in an application.
- Compare startup (AOT vs JIT) and feature support.
Verify: embedded host runs a module with resource limits enforced.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: the runtime list (wazero for Go, wasm3 an interpreter, WasmEdge, Wasmer), `consume_fuel` and `epoch_interruption` and the no-initial-fuel note.
Removed or reworded as unconfirmed: the claim about embedding APIs in Rust, Go, Python and C.
Method: documentation only; no commands were run.
