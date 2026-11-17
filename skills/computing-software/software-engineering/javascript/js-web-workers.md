---
id: computing-software.software-engineering.javascript.js-web-workers
name: js-web-workers
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-web-workers, postmessage, transferable-objects, comlink, offscreen-canvas]
level: advanced
status: docs-checked
description: "Run CPU-bound browser work in Web Workers: constructor URL form, available APIs, structured-clone messages, transferables, errors and terminate."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers", "https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Functions_and_classes_available_to_workers", "https://developer.mozilla.org/en-US/docs/Web/API/Worker/Worker", "https://developer.mozilla.org/en-US/docs/Web/API/Worker/postMessage", "https://developer.mozilla.org/en-US/docs/Web/API/Worker"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Web Workers

- `new Worker(new URL("./w.js", import.meta.url))`: MDN notes bundlers (webpack, Vite, Parcel) recommend this URL form. The constructor runs a classic script or a module; its `type` option selects which.
- A worker cannot manipulate the DOM or use some `window` members. It can use `fetch()` and `XMLHttpRequest` for network requests, WebSockets, IndexedDB, timers such as `setTimeout()`, and `importScripts()`.
- Messages are copied with the structured clone algorithm. To move a large buffer instead of copying, pass it in the transfer list: `worker.postMessage(buf, [buf])`; ownership moves to the receiver and the sender's `byteLength` becomes 0.
- A worker can send replies with `self.postMessage` (`DedicatedWorkerGlobalScope.postMessage`). A runtime error in the worker calls the `onerror` handler with an `ErrorEvent`.
- `worker.terminate()` stops the worker at once, without letting it finish its operation. A worker may spawn sub-workers only from the same origin as its parent page.
- Worker kinds: dedicated, shared (`SharedWorker`, see js-shared-worker-channel) and service workers (separate lifecycle, see js-service-workers-and-caching).

Verify: profile the main thread before and after moving the work.

## Checked

2026-11-03. Confirmed on MDN: Using Web Workers (no DOM, fetch/XHR/IndexedDB/WebSockets, same-origin sub-workers, `terminate()`, `onerror`, `import.meta.url` bundler note), Functions and classes available to workers, Worker() constructor (classic script or module, `type`), Worker.postMessage (structured clone, transfer, detached buffer length 0 in the example), Worker.terminate. Removed: pooling to `navigator.hardwareConcurrency`, Comlink RPC advice, `onmessageerror` handling, the "startup costs milliseconds" figure, the Blob-URL cross-origin workaround, the 50 ms long-task check, `OffscreenCanvas` as a worker capability (only a link on the Worker page), and the ECMAScript and MDN JavaScript root sources.
Method: documentation only; no commands were run.
