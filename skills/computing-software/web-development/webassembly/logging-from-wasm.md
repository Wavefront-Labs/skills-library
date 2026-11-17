---
id: computing-software.web-development.webassembly.logging-from-wasm
name: logging-from-wasm
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, console-log-import, wasi-logging, panic-hooks, wasm-logging, wasm-tracing, opentelemetry-wasm, wasm]
level: practitioner
status: draft
description: "Diagnostics"
sources: ["https://webassembly.github.io/spec/core/", "https://developer.mozilla.org/en-US/docs/WebAssembly", "https://component-model.bytecodealliance.org/", "https://wasi.dev/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Logging and diagnostics

Goal: see what Wasm does.
- Import a log function from the host; use WASI stdout/stderr; in Rust set a panic hook.
- Include request IDs.
- Strip verbose logs in release builds.
Verify: log lines appear with context.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
