---
id: computing-software.web-development.webassembly.host-native-api-registration
name: host-native-api-registration
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wasm-native-api, wasm-c-api, host-import-binding, wasm]
level: practitioner
status: docs-checked
description: "Host bindings"
sources: ["https://raw.githubusercontent.com/bytecodealliance/wasm-micro-runtime/main/doc/export_native_api.md", "https://raw.githubusercontent.com/bytecodealliance/wasm-micro-runtime/main/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Registering native host functions

Goal: expose device functions.
- Register native functions with signatures (for example WAMR `NativeSymbol` tables) or use the standard `wasm_c_api`.
- Validate pointers from Wasm before dereferencing in native code.
- Keep the API minimal.
Verify: invalid pointers from Wasm are rejected.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: `NativeSymbol` tables with signature strings, `wasm_c_api`, `wasm_runtime_validate_app_addr`.
Removed or reworded as unconfirmed: nothing.
Method: documentation only; no commands were run.
