---
id: computing-software.web-development.webassembly.wasm-gc-proposal
name: wasm-gc-proposal
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wasm-gc-types, struct-array-types, kotlin-wasm, wasm-gc, wasm-exception-handling, tail-calls, wasm]
level: practitioner
status: docs-checked
description: "Managed languages"
sources: ["https://raw.githubusercontent.com/WebAssembly/gc/main/proposals/gc/Overview.md", "https://raw.githubusercontent.com/JetBrains/kotlin-web-site/master/docs/topics/wasm/wasm-overview.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WasmGC

Goal: understand GC support.
- The GC proposal aims at efficient support for high-level languages (faster execution, smaller modules) and at giving Wasm access to the engine's existing garbage collector on the web.
- Design: managed data is independent of linear memory; the types describe low-level data layout (structs, arrays, unboxed scalars), not source-language object models; checked down casts are the escape hatch; heap values from the embedder, such as JavaScript objects, are a stated requirement.
- A stated non-goal is seamless interoperability between multiple languages.
- Different from linear-memory languages like C/Rust, which manage their own heap inside linear memory.
- Kotlin/Wasm (Beta in the JetBrains docs) needs a browser that supports the Wasm garbage collection proposal and the legacy exception handling proposal; check the WebAssembly roadmap for current status rather than assuming a version.
Verify: a Kotlin/Wasm sample runs in a browser that supports the proposals it needs.

## Checked

2026-11-08. Confirmed in the GC proposal Overview (read lines 1-120 only: motivation, requirements, approach, types, efficiency, start of use cases) and the Kotlin/Wasm overview (read in full): the aims, design points and non-goal above, and the browser requirement for Kotlin/Wasm.
Removed as unconfirmed: the claim that Dart and Java use it, and any per-browser version support.
Method: documentation only; no commands were run.
