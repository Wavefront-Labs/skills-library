---
id: computing-software.software-engineering.javascript.js-shared-worker-channel
name: js-shared-worker-channel
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, broadcastchannel, js-web-workers]
level: advanced
status: docs-checked
description: "Coordinate tabs and workers with SharedWorker ports, MessageChannel, BroadcastChannel and the Web Locks API."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/BroadcastChannel", "https://developer.mozilla.org/en-US/docs/Web/API/SharedWorker", "https://developer.mozilla.org/en-US/docs/Web/API/MessageChannel", "https://developer.mozilla.org/en-US/docs/Web/API/Web_Locks_API"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SharedWorker, MessageChannel and BroadcastChannel

- `new BroadcastChannel("app")` is a named channel that any browsing context of the same origin can subscribe to (windows, tabs, frames, iframes). `postMessage()` fires a `message` event at every other `BroadcastChannel` object on that channel, not the sender. Call `close()` when finished.
- `SharedWorker` can be reached from several browsing contexts (windows, iframes) that share the exact same origin (protocol, host and port). Communicate through `worker.port`: `port.postMessage()` and `port.onmessage`. If you attach with `addEventListener`, call `port.start()` yourself; the `onmessage` setter starts it implicitly. Inside the worker, handle `connect` (`onconnect`) and take `e.ports[0]`. Dedicated workers cannot construct a `SharedWorker`.
- `const { port1, port2 } = new MessageChannel()` creates two linked `MessagePort`s; keep `port1` and transfer `port2` (for example to an iframe or worker) for private two-way messaging.
- Leader election across tabs: the Web Locks API lets scripts in tabs or workers acquire a named lock with `navigator.locks.request(name, callback)`; the lock is held until the callback (usually async) finishes, so only one holder at a time.

Self-check: open two tabs on the same origin and see a message posted on a `BroadcastChannel` in one arrive in the other.

## Checked

2026-11-03. Confirmed on MDN: BroadcastChannel (same-origin contexts, sender excluded), SharedWorker (same origin requirement, `port`, `start()`, `onconnect`, not constructible from dedicated workers; "support varies" banner), MessageChannel (`port1`, `port2`, transferring a port), Web Locks API (`navigator.locks.request`, leader election pattern). Removed: the claim that SharedWorker was missing in some mobile browsers (MDN says only that support varies).
Method: documentation only; no commands were run.
