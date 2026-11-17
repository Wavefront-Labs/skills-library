---
id: computing-software.web-development.frontend-development.comlink-and-worker-pools
name: comlink-and-worker-pools
category: computing-software
field: web-development
product: frontend-development
tags: [web-workers, off-main-thread, comlink, worker-pool, rpc-workers, hardwareconcurrency, task-queue-workers]
level: practitioner
status: docs-checked
description: "Using Comlink to call worker functions like async APIs, and running parallel jobs on a bounded worker pool sized by hardwareConcurrency."
sources:
  - https://github.com/GoogleChromeLabs/comlink
  - https://developer.mozilla.org/en-US/docs/Web/API/Navigator/hardwareConcurrency
  - https://web.dev/articles/off-main-thread
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Comlink and worker pools

**Goal:** worker code is called like a normal async module, and parallel jobs use all cores without spawning unbounded workers.

## 1. Comlink RPC
```js
// math.worker.js
import * as Comlink from 'comlink';
const api = { async hash(buf) { return crypto.subtle.digest('SHA-256', buf); }, fib(n) { return n < 2 ? n : api.fib(n-1) + api.fib(n-2); } };
Comlink.expose(api);
// main
import * as Comlink from 'comlink';
const math = Comlink.wrap(new Worker(new URL('./math.worker.js', import.meta.url), { type: 'module' }));
console.log(await math.fib(35));
await math.hash(Comlink.transfer(buf, [buf]));   // zero-copy argument
```
- Every call is async and arguments are structured-cloned; use `Comlink.transfer` for big buffers.
- Callbacks must be wrapped with `Comlink.proxy(fn)` and released (`proxy[Comlink.releaseProxy]()`) or they leak.

## 2. A bounded pool
```js
export function createPool(url, size = Math.max(1, (navigator.hardwareConcurrency || 4) - 1)) {
  const idle = Array.from({ length: size }, () => Comlink.wrap(new Worker(url, { type: 'module' })));
  const queue = [];
  const next = () => { if (!idle.length || !queue.length) return; const w = idle.pop(); const { fn, res, rej } = queue.shift();
    fn(w).then(res, rej).finally(() => { idle.push(w); next(); }); };
  return (fn) => new Promise((res, rej) => { queue.push({ fn, res, rej }); next(); });
}
const run = createPool(new URL('./thumb.worker.js', import.meta.url));
await Promise.all(files.map(f => run(w => w.thumbnail(f))));
```
Leave a core for the main thread (the pool above defaults to `hardwareConcurrency` minus one). Each worker loads its own copy of the code and data, so memory grows with pool size.

## 3. When not to
A pool for tiny tasks costs more in messaging than it saves. Measure: batch work into chunks of at least several milliseconds each.

## Verify
- [ ] Performance panel shows N worker threads busy in parallel; main thread idle.
- [ ] Throughput scales with pool size up to core count, then flattens.
- [ ] No growing memory from unreleased Comlink proxies after many calls.

## Checked
2026-10-28. Confirmed on the Comlink README: `Comlink.proxy`, `Comlink.transfer`, `releaseProxy`; MDN `navigator.hardwareConcurrency` page cited for sizing. Pool code is an illustrative sketch, not a library API.
Method: documentation only; no commands were run.
