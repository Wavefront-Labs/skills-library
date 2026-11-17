---
id: computing-software.web-development.webassembly.wasi-http-handlers
name: wasi-http-handlers
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wasi-http-proxy, incoming-handler, outgoing-request, wasi-http, wasi-sockets, outbound-http, wasm]
level: practitioner
status: docs-checked
description: "Serverless HTTP"
sources: ["https://raw.githubusercontent.com/WebAssembly/wasi-http/main/wit/handler.wit", "https://raw.githubusercontent.com/WebAssembly/wasi-http/main/wit/proxy.wit"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WASI HTTP handlers

Goal: write HTTP components.
- Implement `wasi:http/incoming-handler`; make outbound requests via `wasi:http/outgoing-handler`.
Verify: curl to the component returns expected body.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: `wasi:http/incoming-handler`, `outgoing-handler`, `proxy` world.
Removed or reworded as unconfirmed: allow-list, framework and streaming-body sentences.
Method: documentation only; no commands were run.
