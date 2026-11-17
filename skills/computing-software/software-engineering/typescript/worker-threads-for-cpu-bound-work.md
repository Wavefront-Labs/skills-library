---
id: computing-software.software-engineering.typescript.worker-threads-for-cpu-bound-work
name: worker-threads-for-cpu-bound-work
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, nodejs, node-runtime, worker-threads, cpu-bound, piscina, sharedarraybuffer, event-loop-blocking]
level: practitioner
status: verified
description: "Keep the Node event loop responsive by moving CPU-heavy work to worker_threads: messaging, transfer lists, worker pools with Piscina, and when to use processes instead."
sources:
  - https://nodejs.org/api/worker_threads.html
  - https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop
  - https://github.com/piscinajs/piscina
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# worker_threads for CPU-bound work

**Goal:** CPU-heavy tasks (image processing, parsing, hashing, compression) run in parallel without blocking request handling.

## 1. Diagnose first
Symptoms of a blocked loop: latency spikes across all endpoints, timers firing late. Measure:
```ts
import { monitorEventLoopDelay } from "node:perf_hooks";
const h = monitorEventLoopDelay({ resolution: 20 }); h.enable();
setInterval(() => console.log("p99 loop delay ms", h.percentile(99) / 1e6), 10_000);
```
`node --cpu-prof` or clinic.js flame graphs show the hot synchronous function.

## 2. A worker
```ts
// hash-worker.ts
import { parentPort } from "node:worker_threads";
import { scryptSync } from "node:crypto";
parentPort!.on("message", ({ id, password, salt }) => {
  parentPort!.postMessage({ id, hash: scryptSync(password, salt, 64).toString("hex") });
});
```
```ts
import { Worker } from "node:worker_threads";
const w = new Worker(new URL("./hash-worker.js", import.meta.url));
w.on("error", err => log.error(err));
w.on("exit", code => { if (code !== 0) log.error(`worker exited ${code}`); });   // `w.terminate()` exits with code 1, so expect this log on a deliberate stop
```
Spawning a worker costs tens of ms and its own V8 isolate (memory; measured 53 ms for spawn plus one scrypt on this machine); never create one per request.

## 3. Use a pool: Piscina
```ts
import Piscina from "piscina";
const pool = new Piscina({ filename: new URL("./resize.js", import.meta.url).href, maxThreads: os.availableParallelism() - 1 });
app.post("/resize", async (req, res) => res.send(await pool.run({ buf: req.body, width: 400 })));
```
```ts
// resize.js
export default async function ({ buf, width }) { return resizeImage(buf, width); }
```
Pools handle queueing, worker restarts, `maxQueue` backpressure and cancellation via `AbortSignal` (Piscina README; the snippet above ran on Piscina 5.3.2).

## 4. Data transfer
- `postMessage` uses structured clone: copies data. Large buffers: pass in the transfer list to move ownership with zero copy: `port.postMessage(buf, [buf.buffer])` (the sender's view becomes detached; tested, `byteLength` became 0).
- `SharedArrayBuffer` + `Atomics` for shared memory (counters, ring buffers); needs careful synchronisation.
- Functions, class instances with methods, and sockets do not survive cloning.

## 5. Threads vs processes vs native
- Threads: shared process, cheap messaging, crash of native code kills everything.
- `child_process`/`cluster`: isolation, more memory; cluster for scaling an HTTP server across cores (or run N containers).
- Many APIs already run off the main thread: async `zlib` and the callback forms of `crypto` functions use libuv's threadpool (Node docs; pbkdf2 measured below), and sharp queues work until libuv provides a worker thread and then uses libvips' own glib thread pool (sharp docs). Use their async APIs first. Tune `UV_THREADPOOL_SIZE` (default 4) if they queue (measured: 4 parallel pbkdf2 calls took 1.5 s, 8 took 3.3 s, i.e. two waves).

## Gotchas
- TypeScript workers: point at the compiled `.js`, or run via tsx/`--import` loaders that workers also inherit (`execArgv`).
- Unhandled exceptions in a worker emit `error` on the Worker object; without a listener the main process crashes.
- Workers do not share module state; each loads its own copy of modules and config.

## Verify
- Under load, event-loop p99 delay stays below ~20 ms while CPU work runs, and throughput scales with `maxThreads` until cores are saturated.
