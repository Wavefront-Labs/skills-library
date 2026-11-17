---
id: computing-software.software-engineering.typescript.cancellation-with-abortcontroller
name: cancellation-with-abortcontroller
category: computing-software
field: software-engineering
product: typescript
tags: [javascript, abortcontroller, abortsignal, cancellation, fetch-timeout, abortsignal-timeout, abortsignal-any, request-cancellation, nodejs]
level: practitioner
status: verified
description: "Cancel fetches, timers, listeners and your own async functions with AbortController/AbortSignal, including timeouts, combining signals and abort-aware APIs."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/AbortController", "https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal/timeout_static", "https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal/any_static", "https://nodejs.org/api/globals.html#class-abortcontroller"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cancellation with AbortController

**Goal:** stop work nobody needs any more (user navigated away, request timed out,
sibling failed) so it frees sockets and CPU and does not write stale results.

(Every snippet and API below was run on Node 24.22.)

## Basics
```ts
const ac = new AbortController();
const res = await fetch(url, { signal: ac.signal });
ac.abort();                       // fetch rejects with DOMException name "AbortError"
```
Timeouts without manual timers:
```ts
await fetch(url, { signal: AbortSignal.timeout(5_000) });   // rejects with "TimeoutError"
```
Combine a caller's signal with a timeout:
```ts
const signal = AbortSignal.any([callerSignal, AbortSignal.timeout(5_000)]);
```

## Making your own functions abortable
```ts
async function syncAll(items: Item[], signal?: AbortSignal) {
  for (const it of items) {
    signal?.throwIfAborted();                // cheap check at each step
    await upload(it, { signal });           // pass it down to every abort-aware call
  }
}
```
Accept `signal` as the LAST options field, pass it to every API that supports it, and
check `throwIfAborted()` between CPU-bound steps. Register cleanup:
`signal.addEventListener("abort", cleanup, { once: true })`.

## Abort-aware APIs worth knowing
- `fetch`, `addEventListener(type, fn, { signal })` (removes the listener on abort,
  ideal for component teardown)
- Node: `timers/promises` `setTimeout(ms, val, { signal })`, `events.once`,
  `fs.promises.readFile(p, { signal })`, `stream.pipeline(..., { signal })`,
  `child_process.spawn(cmd, args, { signal })`
- React: abort in the `useEffect` cleanup to drop responses for unmounted components.

## Handling the rejection
```ts
try { await work(signal); }
catch (e) {
  if (e instanceof DOMException && (e.name === "AbortError" || e.name === "TimeoutError")) return;
  throw e;
}
```
`ac.abort(reason)` sets `signal.reason`; fetch rejects with that reason (tested: the custom `Error` came back, not an `AbortError`). `timers/promises` `setTimeout` rejects with `AbortError` / code `ABORT_ERR`, as does `readFile(p, { signal })` on an aborted signal.

## Gotchas
- Aborting does not undo server-side effects of a request already received; design
  non-idempotent operations with idempotency keys.
- An AbortController is single-use; create a new one per operation.
- Listeners added to a long-lived signal accumulate; use `{ once: true }` or remove them.

## Verify
- [ ] Navigating away / unmounting cancels in-flight requests (network tab shows "canceled").
- [ ] Timeout tests assert the TimeoutError path and that no late result is applied.
