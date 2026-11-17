---
id: computing-software.web-development.webassembly.wasm-plugin-systems
name: wasm-plugin-systems
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, extism, plugin-sandbox, host-functions, wasm-edge-workers, wasm-plugins, wasm-sandboxing, wasm]
level: practitioner
status: docs-checked
description: "Embedding untrusted code"
sources: ["https://raw.githubusercontent.com/extism/extism/main/README.md", "https://raw.githubusercontent.com/bytecodealliance/wasmtime/main/docs/examples-interrupting-wasm.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wasm as a plugin system

Goal: run third-party plugins safely.
- Extism is a framework on top of standard Wasm runtimes whose README names building extensible software and plugins that run untrusted user code as a primary use case.
- Extism adds persistent memory and module-scope variables, host-controlled HTTP without WASI, runtime limiters and timers, and simpler host function linking.
- Split: hosts use an SDK (many languages); plugin authors compile a PDK (Plug-in Development Kit) into the `.wasm` to read input, config and variables and return data.
- A schema (XTP Bindgen) can generate PDK bindings so the host/plugin function signatures are versioned in one place.
- If you use Wasmtime directly, fuel and epoch interruption bound execution time (see the interrupting-Wasm page).
- Keep the host function surface narrow and version the plugin interface.
Verify: a hostile plugin cannot exceed its limits.

## Checked

2026-11-08. Confirmed in the Extism README (read in full) and the Wasmtime interrupting page (read in full).
Removed as unconfirmed: the claim that Extism uses a specific plugin ABI, and any memory-limit API names.
Method: documentation only; no commands were run.
