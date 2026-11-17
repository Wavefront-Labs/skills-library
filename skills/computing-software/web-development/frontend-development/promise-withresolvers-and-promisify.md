---
id: computing-software.web-development.frontend-development.promise-withresolvers-and-promisify
name: promise-withresolvers-and-promisify
category: computing-software
field: web-development
product: frontend-development
tags: [promise-withresolvers, promisify, deferred-promise, events-once, timers-promises, javascript]
level: practitioner
status: docs-checked
description: "Turning callbacks and events into promises: Promise.withResolvers, util.promisify, events.once, timers/promises, and avoiding the explicit-construction antipattern."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/withResolvers
  - https://nodejs.org/api/util.html#utilpromisifyoriginal
  - https://nodejs.org/api/events.html#eventsonceemitter-name-options
  - https://nodejs.org/api/timers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Promise.withResolvers and promisifying

## 1. Promise.withResolvers (ES2024, Baseline 2024)
```js
const { promise, resolve, reject } = Promise.withResolvers();
socket.addEventListener("open", () => resolve(socket), { once: true });
socket.addEventListener("error", reject, { once: true });
await promise;
```
Replaces the "deferred" pattern of capturing `resolve` out of a `new Promise` executor. Use it when resolution happens in a different scope (queues, request/response correlation by id).

## 2. Wrapping callback APIs
```js
import { promisify } from "node:util";
import { execFile } from "node:child_process";
const run = promisify(execFile);
const { stdout } = await run("git", ["rev-parse", "HEAD"]);
```
Most Node core APIs already have promise versions: `node:fs/promises`, `node:dns/promises`, `node:stream/promises` (`pipeline`, `finished`), `node:timers/promises`.

## 3. Events and timers
```js
import { once } from "node:events";
const [req] = await once(server, "request", { signal: AbortSignal.timeout(5000) });

import { setTimeout as sleep } from "node:timers/promises";
await sleep(250, undefined, { signal });

// browser
const sleepB = ms => new Promise(r => setTimeout(r, ms));
const loaded = new Promise(r => img.addEventListener("load", r, { once: true }));
```

## 4. Antipatterns
```js
// explicit construction around something that already returns a promise
return new Promise((res, rej) => fetch(u).then(res).catch(rej));   // just: return fetch(u)
// a throw inside a later callback is not caught by the promise
new Promise(() => setTimeout(() => { throw new Error("lost"); }));  // uncaught exception, promise never settles
```
A synchronous throw inside the executor rejects the promise; one thrown from a later callback does not.

## Gotchas
- A promise resolves once; later `resolve` calls are ignored, so check listeners are removed (`{ once: true }`, `AbortSignal`).
- Never-settling promises leak closures; pair with `AbortSignal.timeout` or `Promise.race` timeouts.

## Verify
- [ ] Each wrapper settles on both success and error paths; tests cover timeout/abort.

## Checked

2026-10-26. MDN Promise.withResolvers (resolve and reject live in the same scope as the promise) and browser-compat-data (Chrome 119, Firefox 121, Safari 17.4), Node docs (util.promisify; promisified child_process.exec/execFile return stdout and stderr; events.once(emitter, name[, options]) accepts a signal; timers/promises). Rewrote the async-throw antipattern comment to describe the behaviour precisely.

Method: documentation only; no commands were run.
