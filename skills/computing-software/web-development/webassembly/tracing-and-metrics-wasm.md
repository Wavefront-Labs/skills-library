---
id: computing-software.web-development.webassembly.tracing-and-metrics-wasm
name: tracing-and-metrics-wasm
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, otel-wasm, host-metrics, span-propagation, wasm]
level: practitioner
status: draft
description: "Telemetry"
sources: ["https://webassembly.github.io/spec/core/", "https://developer.mozilla.org/en-US/docs/WebAssembly", "https://component-model.bytecodealliance.org/", "https://wasi.dev/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tracing and metrics

Goal: measure behaviour.
- Host emits spans around calls; propagate trace context into the component via arguments or WASI HTTP headers.
- Export runtime metrics (instances, memory, fuel).
- Sample to limit overhead.
Verify: traces link host and guest work.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
