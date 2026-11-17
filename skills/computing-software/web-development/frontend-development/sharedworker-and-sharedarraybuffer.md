---
id: computing-software.web-development.frontend-development.sharedworker-and-sharedarraybuffer
name: sharedworker-and-sharedarraybuffer
category: computing-software
field: web-development
product: frontend-development
tags: [web-workers, off-main-thread, sharedworker, sharedarraybuffer, atomics, cross-origin-isolation, crossoriginisolated]
level: practitioner
status: docs-checked
description: "Sharing one worker across tabs with SharedWorker, and shared memory with SharedArrayBuffer/Atomics under cross-origin isolation (COOP/COEP)."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/SharedWorker
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer
  - https://web.dev/articles/coop-coep
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SharedWorker and SharedArrayBuffer

**Goal:** share one connection/state across tabs (SharedWorker) or share memory between threads (SharedArrayBuffer) without races.

## 1. SharedWorker
```js
// page
const sw = new SharedWorker(new URL('./hub.worker.js', import.meta.url), { type: 'module', name: 'hub' });
sw.port.onmessage = (e) => render(e.data);
sw.port.start();
// hub.worker.js
const ports = new Set();
self.onconnect = (e) => { const p = e.ports[0]; ports.add(p); p.onmessage = (m) => broadcast(m.data); p.start(); };
const broadcast = (d) => ports.forEach(p => p.postMessage(d));
```
All browsing contexts that use a SharedWorker must share the exact same origin, and the optional `name` identifies the worker scope (useful for creating separate instances of the same script). Typical use: one WebSocket for all tabs. Check MDN's compatibility table for your target browsers, and keep a fallback: Web Locks leader election + BroadcastChannel. Design for tabs disappearing: send a goodbye on `pagehide` and expire silent ports. Without `extendedLifetime`, the worker is not kept alive after all references close.

## 2. SharedArrayBuffer needs cross-origin isolation
MDN: shared memory requires a secure context that is cross-origin isolated (`crossOriginIsolated === true`), which needs these headers on the top-level document; without them the `SharedArrayBuffer` constructor is hidden and `postMessage()` throws for `SharedArrayBuffer` objects:
```
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp      (or credentialless)
```
With `require-corp`, cross-origin resources requested in `no-cors` mode must carry a `Cross-Origin-Resource-Policy` header (or be loaded via CORS). With `credentialless`, no-cors cross-origin resources load without explicit CORP permission but the request is sent without credentials (cookies omitted and ignored in the response). Test any popup-based OAuth or payment flow after adding COOP.

## 3. Atomics
```js
const sab = new SharedArrayBuffer(4 * 1024); const ia = new Int32Array(sab);
worker.postMessage(sab);                  // shared, not copied or transferred
Atomics.add(ia, 0, 1);                    // race-free increment
Atomics.wait(ia, 1, 0);                   // blocks: not allowed on the main thread
Atomics.notify(ia, 1, 1);
```
Plain reads/writes on shared memory race; use `Atomics` for anything coordinated. `Atomics.wait()` is blocking and cannot be used on the main thread; `Atomics.waitAsync()` is non-blocking.

## Verify
- [ ] `crossOriginIsolated` logs `true`; no COEP-blocked resources in the console.
- [ ] Two tabs share one WebSocket (server sees one connection).
- [ ] OAuth popup flow still works after adding COOP (or uses a redirect flow).

## Checked

Checked 2026-10-26 against MDN SharedWorker and SharedWorker() constructor, SharedArrayBuffer, Atomics.wait(), Atomics.waitAsync() and Cross-Origin-Embedder-Policy (mdn/content main): same-origin requirement, `name`, `extendedLifetime`, cross-origin-isolation requirement and its effect on the constructor and postMessage, `require-corp` versus `credentialless`, and the main-thread restriction on `Atomics.wait()`. Removed the unconfirmed Chrome-on-Android and Safari 16 support claims, the 'one instance per origin + URL + name' wording, and the OAuth-popup breakage assertion (kept as a test).

Method: documentation only; no commands were run.
