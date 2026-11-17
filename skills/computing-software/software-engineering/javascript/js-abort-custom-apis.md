---
id: computing-software.software-engineering.javascript.js-abort-custom-apis
name: js-abort-custom-apis
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, abort-listener-cleanup, js-abort]
level: advanced
status: docs-checked
description: "Accept a signal in custom async functions and tear down listeners with it."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal", "https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal/throwIfAborted", "https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cancellation in your own APIs and listeners

- Pattern: `async function job({ signal } = {}) { signal?.throwIfAborted(); await step(); signal?.throwIfAborted(); }`. `throwIfAborted()` throws the signal's abort reason if aborted and does nothing otherwise, so it can mark cancellation points in a loop.
- Promise-based APIs reject any unsettled promise with the signal's abort reason: call `signal.throwIfAborted()` first (already aborted), then `signal.addEventListener("abort", onAbort, { once: true })` where `onAbort` clears timers and calls `reject(signal.reason)`.
- `{ once: true }` removes the listener only when the abort fires. Remove it yourself (`signal.removeEventListener("abort", onAbort)`) when the operation completes normally, ideally in `finally`, so a long-lived signal does not retain the listener and what it references.
- Reuse one signal to remove many listeners: `el.addEventListener("click", fn, { signal })`; calling `abort()` on the owning controller removes them.
- A signal is single-use: once aborted, fetch calls using it reject immediately. Create a new `AbortController` per operation.
- Combine cancellation sources with `AbortSignal.any([a, b])`; `AbortSignal.timeout(ms)` aborts with a `TimeoutError` (user aborts give `AbortError`), but a signal from `any()` cannot tell you whether a timeout caused the abort.
- Signals owned by a controller are garbage collectible once signal and controller are unreachable; signals from `any()` or `timeout()` are kept alive while they have listeners (and, for `timeout()`, a pending timeout).

Self-check: aborting midway leaves no pending timers or listeners.

## Checked

Checked 2026-11-09 against MDN AbortSignal, AbortSignal.throwIfAborted() and EventTarget.addEventListener (the `signal` option), read in full for the relevant sections.
Confirmed: every point above, including the `myCoolPromiseAPI` pattern, the `{ once: true }` caveat, `any()`/`timeout()` behaviour and single-use signals.
Removed as unconfirmed: the claim that Node APIs (`fs/promises`, `events.once`, timers/promises) accept `signal` (MDN page does not cover them).

Method: documentation only; no commands were run.
