---
id: computing-software.web-development.webassembly.embedding-in-other-languages
name: embedding-in-other-languages
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wasmtime-py, wasmtime-go, wasmer-java, wasm]
level: practitioner
status: docs-checked
description: "Host embedding"
sources: ["https://raw.githubusercontent.com/bytecodealliance/wasmtime/main/docs/lang.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Embedding runtimes in host languages

Goal: call Wasm from other languages.
- Wasmtime is written in Rust (`wasmtime` crate). Officially supported bindings in its own repository: Rust, C (`libwasmtime.a`, the entry point for other languages) and C++ (headers layered on the C API).
- External bindings developed outside the repository, which may lag in features and release timing: Python (`wasmtime` on PyPI), Go (wasmtime-go), .NET (`Wasmtime` NuGet package, .NET Core SDK 3.0 or later), Ruby (RubyGems) and Elixir (Hex).
- The C API is not always in parity with the Rust API.
- Define host functions, memory access and limits through the binding in use; version-lock the runtime and any WIT bindings. Other runtimes such as Wasmer are not covered by the source read here.
Verify: the host calls an exported function and reads memory.

## Checked

2026-11-08. Confirmed in the Wasmtime "Using the Wasmtime API" page (read in full).
Removed as unconfirmed: wasmer-java and other Wasmer language claims.
Method: documentation only; no commands were run.
