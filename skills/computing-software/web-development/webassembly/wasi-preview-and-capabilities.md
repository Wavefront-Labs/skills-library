---
id: computing-software.web-development.webassembly.wasi-preview-and-capabilities
name: wasi-preview-and-capabilities
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wasi-preview1, preopened-directories, capability-security, wasi, wasmtime, wasmer, wasm]
level: practitioner
status: docs-checked
description: "System interface"
sources: ["https://raw.githubusercontent.com/WebAssembly/WASI/main/docs/Capabilities.md", "https://raw.githubusercontent.com/bytecodealliance/wasmtime/main/docs/cli-options.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WASI capabilities and preopens

Goal: run Wasm outside the browser.
- Wasm has no syscall instructions or built-in I/O; programs get capabilities. Link-time capabilities are imported functions (in the component model, instance imports); runtime capabilities are unforgeable handles passed around at runtime.
- Use handles when several distinct resources must be live at once (open files); link-time capabilities suit APIs with one obvious instance, such as a clock.
- Wasmtime CLI: all Wasmtime options must come before the Wasm file; anything after it goes to the program. To mount the current directory use `wasmtime --dir . foo.wasm`, not `wasmtime foo.wasm --dir .`.
- Core modules receive arguments through WASIp1 APIs; components through WASIp2 or later, and a component runs through `wasi:cli/run`. `wasmtime run --invoke <export>` calls a specific export instead (the syntax is documented as unstable).
Verify: the program can reach only directories that were granted.

## Checked

2026-11-08. Confirmed in WASI Capabilities.md (read in full) and the Wasmtime CLI page (read lines 55-115 only: running modules and components, argument order, `--dir`, `--invoke`).
Removed as unconfirmed: `--env KEY=val`, the `--dir=./data` form and the "preview 2 is component-model based" sentence.
Method: documentation only; no commands were run.
