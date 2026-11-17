---
id: computing-software.software-engineering.v-lang.v-wasm-wasi-target
name: v-wasm-wasi-target
category: computing-software
field: software-engineering
product: v-lang
tags: [v-wasm-wasi-target, webassembly-backend, wasi, wasmtime, wasmer, -os wasi, wasm runtime, command line wasm, v-lang]
level: advanced
status: draft
description: "Build a WASI module with -os wasi, run with wasmtime or wasmer, and understand fs and stdout limitations."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# WASI target and running with runtimes

Goal: ship portable command-line wasm.

- `v -b wasm -os wasi -o app.wasm app.v` then `wasmtime app.wasm` or `wasmer app.wasm` (confirm exact flags).
- `println` maps to WASI `fd_write`; args and env via WASI imports are supported when the runtime passes them.
- Filesystem access requires pre-opened dirs: `wasmtime --dir=. app.wasm`.
- Keep to the subset of builtin the wasm backend supports (strings, arrays, simple structs); check the backend's "unsupported" compile errors.
- Test in CI with the same runtime version you ship against.

Gotchas:
- Features such as threads, sockets and `os.exec` are unavailable.
- Backend maturity varies by release; pin the V version.

Verify: run under wasmtime and compare output with the native build.
