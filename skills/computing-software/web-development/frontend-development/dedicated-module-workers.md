---
id: computing-software.web-development.frontend-development.dedicated-module-workers
name: dedicated-module-workers
category: computing-software
field: web-development
product: frontend-development
tags: [web-workers, off-main-thread, dedicated-worker, module-worker, worker-bundling, import-meta-url, worker-errors]
level: practitioner
status: docs-checked
description: "Moving CPU work off the main thread with dedicated module workers: creating them so bundlers resolve them, messaging, errors and lifecycle."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers
  - https://web.dev/learn/performance/web-worker-overview
  - https://vite.dev/guide/features.html#web-workers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dedicated module workers

**Goal:** heavy computation (parsing, diffing, image processing, search indexing) runs in a worker so input stays responsive.

## 1. Create the worker so bundlers find it
```js
const worker = new Worker(new URL('./search.worker.js', import.meta.url), { type: 'module' });
```
Vite documents this `new Worker(new URL('./worker.js', import.meta.url), { type: 'module' })` form and bundles the worker as its own entry; check your bundler's documentation for its own support. Module workers (`type: 'module'`) allow `import` in the worker.

## 2. Message protocol
```js
// main
let seq = 0; const pending = new Map();
worker.onmessage = ({ data }) => { const p = pending.get(data.id); pending.delete(data.id); data.error ? p.reject(new Error(data.error)) : p.resolve(data.result); };
export const search = (q) => new Promise((resolve, reject) => { const id = ++seq; pending.set(id, { resolve, reject }); worker.postMessage({ id, q }); });

// search.worker.js
import { buildIndex } from './index.js';
const index = buildIndex();
self.onmessage = ({ data }) => {
  try { self.postMessage({ id: data.id, result: index.search(data.q) }); }
  catch (e) { self.postMessage({ id: data.id, error: String(e) }); }
};
```
Correlate requests with ids; replies can come back out of order if the worker does async work.

## 3. Errors and lifecycle
- `worker.onerror` fires when an error occurs in the worker; `onmessageerror` fires when the worker receives a message that can't be deserialised. For Vite's worker detection, `new URL()` must be written directly inside `new Worker()` and the options must be static values.
- `worker.terminate()` kills it immediately (cancel long jobs by terminating and recreating).
- Workers have no DOM, no `window`, no `localStorage`; they have `fetch`, IndexedDB, `setTimeout`, WebSockets, and the other APIs MDN lists as available to workers.

## 4. When it pays off
Workers cost startup time and message copying (measure both). Worth it for long or repeated tasks. For short tasks, yielding on the main thread may be simpler.

## Verify
- [ ] Performance panel: the heavy task appears on the worker thread, main-thread long tasks gone.
- [ ] Production build emits a separate worker chunk and it loads (no 404/MIME error).
- [ ] Thrown errors in the worker reject the right promise.

## Checked

Checked 2026-10-26 against the MDN Using Web Workers and Worker() constructor pages and the Vite web-workers section (features.md in vitejs/vite docs): `new URL(..., import.meta.url)` with `{ type: 'module' }`, no DOM or window in workers, `terminate()`, `onerror` and `onmessageerror`. Removed unconfirmed startup-cost figures, the all-browsers support statement and the list of bundlers beyond Vite.

Method: documentation only; no commands were run.
