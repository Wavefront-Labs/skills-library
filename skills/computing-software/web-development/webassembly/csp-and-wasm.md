---
id: computing-software.web-development.webassembly.csp-and-wasm
name: csp-and-wasm
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wasm-unsafe-eval, csp-script-src, trusted-types-wasm, wasm]
level: practitioner
status: docs-checked
description: "Allow WebAssembly under a Content Security Policy with the 'wasm-unsafe-eval' script-src source instead of 'unsafe-eval'."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/script-src
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Content Security Policy for Wasm

Goal: allow Wasm under CSP.
- If a page has a CSP header and `'wasm-unsafe-eval'` is not in `script-src`, WebAssembly is blocked from loading and executing on the page. Example: `Content-Security-Policy: script-src 'wasm-unsafe-eval'`.
- `'unsafe-eval'` also permits Wasm compilation and instantiation but is broader (it also allows `eval` and similar string-to-code methods) and overrides any `'wasm-unsafe-eval'` in the policy. Prefer the narrower `'wasm-unsafe-eval'`.
Verify: no CSP violations while Wasm still loads.

## Checked
Read the `'unsafe-eval'` and `'wasm-unsafe-eval'` sections of the MDN script-src page (lines covering both source expressions) on 2026-11-08; the rest of the page was not read. Confirmed the blocking behaviour, the example header and the relationship between the two keywords. Removed: Subresource Integrity advice, report-only testing advice, the Trusted Types tag claim, and the generic spec/component-model/WASI sources, none of which was read for this skill.
Method: docs-only read of cited pages, 2026-11-08
