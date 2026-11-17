---
id: computing-software.web-development.frontend-development.async-mutex-and-single-flight
name: async-mutex-and-single-flight
category: computing-software
field: web-development
product: frontend-development
tags: [async-mutex, single-flight, web-locks-api, request-deduplication, race-conditions, javascript]
level: practitioner
status: verified
description: "Serialising async work in JavaScript: promise-chain mutexes, single-flight deduplication of concurrent requests, token refresh races and the Web Locks API across tabs."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Web_Locks_API
  - https://github.com/DirtyHairy/async-mutex
  - https://pkg.go.dev/golang.org/x/sync/singleflight
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Async mutex and single-flight

JS is single-threaded but `await` interleaves: two handlers can both read state, await, then both write.

## 1. Promise-chain mutex
```js
function createMutex() {
  let tail = Promise.resolve();
  return fn => {
    const run = tail.then(fn);             // runs after the previous task settled
    tail = run.catch(() => {});            // keep the chain alive: tail never rejects, so a failure does not block later tasks
    return run;
  };
}
const lock = createMutex();
await lock(async () => { const v = await read(); await write(v + 1); });
```
Library: `async-mutex` (`Mutex`, `Semaphore`, `withTimeout`).

## 2. Single-flight (dedupe concurrent identical calls)
```js
const inflight = new Map();
function once(key, fn) {
  if (inflight.has(key)) return inflight.get(key);
  const p = fn().finally(() => inflight.delete(key));
  inflight.set(key, p);
  return p;
}
```
Classic use: **token refresh**. Ten requests get 401 at once; only one refresh call should happen and all ten retry with the new token:
```js
const refresh = () => once("refresh", () => fetch("/auth/refresh", { method: "POST" }).then(r => r.json()));
```

## 3. Across tabs: Web Locks
```js
await navigator.locks.request("token-refresh", async () => {
  if (!tokenStillExpired()) return;        // another tab may have refreshed already
  await doRefresh();
});
```
Run in Node 24 (`navigator.locks` exists there; ran two contending requests, strictly serialised, and `ifAvailable`/`signal` behaved as listed: callback got `null`, aborted request rejected with `AbortError`). Lock is released when the callback's promise settles or the tab closes. Options: `{ ifAvailable: true }`, `{ mode: "shared" }`, `{ signal }`. Baseline 2022.

## 4. Latest-wins instead of locking
For search-as-you-type, cancel the stale request (`AbortController`) or ignore responses whose request id is not the latest; do not queue them.

## Gotchas
- A mutex around code that never settles deadlocks everything after it: add timeouts.
- Re-entrancy: calling `lock()` inside a locked section deadlocks (ran it: the promise never settled). Callers of `lock()` still see their own task's error.
- Server-side Node with several processes needs a distributed lock (DB row lock, Redis), not an in-memory mutex.

## Verify
- [ ] Test fires N concurrent calls and asserts the underlying function ran once (single-flight) or sequentially (mutex).
