---
id: computing-software.software-engineering.javascript.js-atomics-and-sharedarraybuffer
name: js-atomics-and-sharedarraybuffer
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-atomics, sharedarraybuffer, cross-origin-isolation, lock-free]
level: sme
status: gated
description: "Share memory between workers with SharedArrayBuffer and Atomics, and meet the cross-origin isolation requirement."
sources: ["https://tc39.es/ecma262/", "https://developer.mozilla.org/en-US/docs/Web/JavaScript"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SharedArrayBuffer and Atomics

- `SharedArrayBuffer` memory is visible to multiple threads (Workers). Plain reads/writes race; use `Atomics.add/sub/and/or/xor/exchange/compareExchange/load/store` on integer typed arrays for atomic operations.
- Blocking: `Atomics.wait(ta, idx, expected, timeout)` blocks the calling thread (not allowed on the browser main thread; allowed in workers); `Atomics.notify(ta, idx, count)` wakes waiters. `Atomics.waitAsync` is the non-blocking variant where supported.
- Browsers expose SharedArrayBuffer only on cross-origin isolated pages: send `Cross-Origin-Opener-Policy: same-origin` and `Cross-Origin-Embedder-Policy: require-corp` (or `credentialless`); check `self.crossOriginIsolated`. Third-party embeds then need CORP/CORS headers.
- Build mutexes with `compareExchange` on an Int32Array slot; avoid spinning without `wait`.
- Prefer `postMessage` with transferables or structured cloning unless profiling shows copying is the bottleneck.

## Checked

- Date: 2026-11-02.
- Source pages listed in `sources` were fetched where possible; ECMA-262 (too large to read) and the MDN landing page only; Atomics method signatures and COOP/COEP header values not checked. Treat the specific names, flags and figures as unconfirmed (gated: unconfirmed, source is paywalled or blocked).

Method: documentation only; no commands were run.
