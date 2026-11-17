---
id: computing-software.web-development.webassembly.wasm-edge-serverless
name: wasm-edge-serverless
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, spin-framework, cloudflare-workers-wasm, wasi-http, wasm]
level: practitioner
status: docs-checked
description: "Edge compute"
sources: ["https://raw.githubusercontent.com/spinframework/spin/main/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Edge and serverless runtimes

Goal: deploy Wasm at the edge.
- Spin is a framework for building, deploying and running cloud microservices with WebAssembly, built on the component model; SDKs exist for several languages.
- Workflow from the README: `spin new --accept-defaults -t http-rust hello-rust` creates an app from a template, `spin build` builds it, `spin up` runs it locally.
- For other platforms (Cloudflare Workers, Fastly Compute) read each vendor's current limits for size, CPU and memory; this skill does not state them.
- Keep state in external stores.
Verify: the deployed endpoint answers within the latency target.

## Checked

2026-11-08. Confirmed in the Spin README (read the overview and the quick-start commands at lines 1-80; the remainder was not read).
Removed as unconfirmed: Fastly `fastly compute` commands, Cloudflare Workers specifics and the cold-start claim.
Method: documentation only; no commands were run.
