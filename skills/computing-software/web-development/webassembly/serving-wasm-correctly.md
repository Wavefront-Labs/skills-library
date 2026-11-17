---
id: computing-software.web-development.webassembly.serving-wasm-correctly
name: serving-wasm-correctly
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, application-wasm-mime, brotli-wasm, cache-control-wasm, wasm-mime-type, csp-wasm, cache-headers, wasm]
level: practitioner
status: docs-checked
description: "Serve Wasm with the application/wasm MIME type for streaming, and set COOP/COEP for shared memory."
sources:
  - https://developer.mozilla.org/en-US/docs/WebAssembly/Reference/JavaScript_interface/instantiateStreaming_static
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Embedder-Policy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Serving Wasm correctly

Goal: deploy so streaming compilation and shared memory work.
- Serve `.wasm` files with `Content-Type: application/wasm`. `WebAssembly.instantiateStreaming()` rejects with a `TypeError` if the response has an incorrect MIME type.
- Shared memory (`SharedArrayBuffer`, used by Wasm threads) requires a secure context and a cross-origin isolated document (check `crossOriginIsolated`). Cross-origin isolation is set with the `Cross-Origin-Opener-Policy` header (`same-origin`) and the `Cross-Origin-Embedder-Policy` header (for example `require-corp`); with `require-corp`, cross-origin `no-cors` subresources need the CORP header.
Verify: the Network panel shows the Wasm response with `application/wasm`, and `crossOriginIsolated` is `true` when threads are used.

## Checked
Read the MIME-type parts of the MDN instantiateStreaming page (the rejection rule and the application/wasm note), the security-requirements section of the SharedArrayBuffer page, and the COOP and COEP header pages' directive lists, on 2026-11-08; these pages were not read end to end. Confirmed the MIME-type rejection, the secure-context and cross-origin-isolation requirements, and the COOP `same-origin` and COEP `require-corp` roles. Removed: Brotli compression, immutable hashed filename caching, `Cache-Control`, the CORS bullet and browser-support advice (no cited page read for them), and the generic spec sources.
Method: docs-only read of cited pages, 2026-11-08
