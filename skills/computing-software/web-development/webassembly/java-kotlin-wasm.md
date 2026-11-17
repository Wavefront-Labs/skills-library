---
id: computing-software.web-development.webassembly.java-kotlin-wasm
name: java-kotlin-wasm
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, teavm, cheerpj, kotlin-wasm-target, wasm]
level: practitioner
status: docs-checked
description: "JVM languages"
sources: ["https://raw.githubusercontent.com/JetBrains/kotlin-web-site/master/docs/topics/wasm/wasm-overview.md", "https://raw.githubusercontent.com/konsoletyper/teavm/master/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Java and Kotlin

Goal: pick a JVM-to-Wasm path.
- Kotlin/Wasm (Beta in the JetBrains docs) compiles Kotlin to Wasm. Browser target: `wasm-js`, used by Compose Multiplatform for web; outside the browser it uses a Wasm-WASI target. Running in a browser needs a version that supports the Wasm garbage collection and legacy exception handling proposals.
- Kotlin/Wasm also has an experimental Component Model path (WASI 0.2, for example a `wasi:http` server sample).
- TeaVM has its own reimplementation of the Java class library (not OpenJDK), so check its class library compatibility report for the APIs you use; its embedding APIs are documented as unstable.
- CheerpJ is not covered by a source here; consult its documentation.
- Compare size, GC strategy and library coverage; keep the interop surface small.
Verify: a sample app runs in the browsers you support.

## Checked

2026-11-08. Confirmed in the Kotlin/Wasm overview (read in full) and the TeaVM README (read in full).
Removed as unconfirmed: "TeaVM compiles Java bytecode ahead of time" and all CheerpJ claims.
Method: documentation only; no commands were run.
