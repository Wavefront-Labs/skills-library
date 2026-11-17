---
id: computing-software.web-development.node-express.async-patterns-streams-and-event-loop-blocking
name: async-patterns-streams-and-event-loop-blocking
category: computing-software
field: web-development
product: node-express
tags: [express, node, async, streams, event-loop, backpressure, worker-threads, unhandled-rejection, performance, web-development]
level: advanced
status: verified
description: "Keeping the Node event loop unblocked in Express: streaming large payloads with backpressure, offloading CPU work, and catching async errors."
sources:
  - https://nodejs.org/en/learn/modules/backpressuring-in-streams
  - https://expressjs.com/en/guide/error-handling.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Async patterns, streams, and not blocking the event loop

**Goal:** a single Express process serves many concurrent requests only if nothing
hogs the one event-loop thread — I/O is fine (it's async), CPU is not.

## 1. What actually blocks the event loop
I/O (DB queries, HTTP calls, fs reads via promises) doesn't block — it's handled
by libuv off-thread and resumes the loop on completion. What blocks is synchronous
CPU work on the main thread: `JSON.parse`/`stringify` on megabyte payloads,
regex backtracking, image processing, synchronous crypto, big in-memory sorts,
`fs.readFileSync`. One request doing this delays every other in-flight request —
Node has one event loop thread regardless of how many requests are "concurrent."
Diagnose with `--prof`/clinic.js or just watching p99 latency spike under load
while CPU sits at 100% on one core.

## 2. Offload CPU work, don't just "await" it
`await` doesn't make synchronous code non-blocking — wrapping a blocking function
in a promise doesn't change where it runs.
```js
// still blocks the loop for the duration of the sync work inside:
async function resize(buf) { return sharp(buf).resize(800).toBuffer(); } // sharp's native call is actually offloaded; verify per-library
```
For genuinely blocking pure-JS work, use `worker_threads` (CPU-bound, shares
memory via `SharedArrayBuffer` if needed) or a separate process/queue (BullMQ +
Redis) for anything that takes more than a few ms — image processing, PDF
generation, large CSV parsing, bcrypt with a high cost factor on the main thread.

## 3. Streaming large responses — don't buffer then send
```js
app.get('/export', async (req, res) => {
  res.setHeader('Content-Type', 'text/csv');
  const stream = db.query('SELECT * FROM orders').stream(); // driver-dependent
  stream.pipe(csvTransform).pipe(res);
  stream.on('error', (err) => { req.destroy(err); }); // don't leave the response hanging
});
```
Building a full array in memory (`rows.map(...).join('\n')`) for a large export
is the common way a "it worked in dev" export OOMs in production on real data
volume. `pipe()` handles backpressure automatically — if the client is slow, the
upstream read pauses rather than piling buffered data into memory.

## 4. Backpressure, manually, when you can't `pipe()`
If you must write in a loop instead of piping, check the return value:
```js
if (!res.write(chunk)) {
  await new Promise((resolve) => res.once('drain', resolve)); // pause until the client catches up
}
```
Ignoring the `false` return and writing anyway defeats backpressure and can grow
an unbounded internal buffer for a slow client.

## 5. Async errors Express won't catch for you
In Express 4, a thrown error inside an `async` route handler becomes an unhandled
promise rejection, not a call to your error middleware — Express's own try/catch
around handlers is synchronous only. Ran on express 4.22.3: `unhandledRejection` fired and the client never got a response.
```js
app.get('/x', async (req, res, next) => {
  try { res.json(await risky()); } catch (err) { next(err); } // must forward explicitly
});
```
Wrap every async handler (or use a helper like `express-async-handler`), or
upgrade to Express 5, which does forward rejected promises to `next` automatically (ran on 5.3.0: the same throwing handler reached the error middleware and returned 500)
— check your version before assuming this is handled.

## 6. Unhandled rejections at the process level
`process.on('unhandledRejection', ...)` should log and alert, not silently
continue — as of recent Node major versions, an unhandled rejection terminates the
process by default (ran on Node 24: exit code 1 with no handler), which is one more reason every awaited call site needs a
catch or forwarding path.

## Verify
- [ ] No synchronous CPU-heavy call sits in a hot request path on the main thread; it's offloaded to a worker/queue.
- [ ] Large exports/downloads stream via `pipe()`, never buffer the full dataset in memory first.
- [ ] Every async route handler forwards errors to `next(err)` (or runs on Express 5's native support).
- [ ] A process-level `unhandledRejection`/`uncaughtException` handler logs and triggers alerting, not silent swallow.
- [ ] Manual stream writes check the `write()` return value and wait on `drain` when `false`.
