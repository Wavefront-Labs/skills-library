---
id: computing-software.web-development.webassembly.wasi-sockets-and-async
name: wasi-sockets-and-async
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wasi-tcp, wasi-poll, wasi-io-streams, wasm]
level: practitioner
status: docs-checked
description: "Networking"
sources: ["https://raw.githubusercontent.com/WebAssembly/wasi-sockets/main/README.md", "https://raw.githubusercontent.com/WebAssembly/wasi-io/main/README.md", "https://raw.githubusercontent.com/WebAssembly/wasi-sdk/main/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sockets and async I/O

Goal: use network APIs.
- Preview 2 sockets and `wasi:io` pollables/streams; preview 3 adds async component-model support (wasi-sdk has a `wasm32-wasip3` target).
Verify: allowed destinations succeed and others fail.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: wasi-sockets TCP/UDP, `wasi:io` pollables and streams, the preview 3 async target.
Removed or reworded as unconfirmed: host destination restriction and HTTP client fallback sentences.
Method: documentation only; no commands were run.
