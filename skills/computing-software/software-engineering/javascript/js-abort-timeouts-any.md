---
id: computing-software.software-engineering.javascript.js-abort-timeouts-any
name: js-abort-timeouts-any
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, abortsignal-any, js-abort]
level: advanced
status: docs-checked
description: "Combine cancellation sources with AbortSignal.any and AbortSignal.timeout, read the abort reason, and remove listeners from combined signals."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal/any_static"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AbortSignal timeout and any

- `AbortSignal.any(iterable)` takes an iterable (such as an Array) of abort signals and returns a signal that aborts when any input aborts. Its reason is the reason of the first signal that aborted.
- If any given signal is already aborted, the returned signal is already aborted, with that signal's reason.
- MDN example: combine a user-cancel `AbortController` signal with `AbortSignal.timeout(1_000 * 60 * 5)` and pass the result as `signal` to `fetch`.
- In the catch block MDN distinguishes `e.name === "AbortError"` (cancelled by the user) from `e.name === "TimeoutError"` (timed out).
- `AbortSignal.any()` has no method to unsubscribe the returned signal from its inputs. Aborting the combined signal does not abort the inputs or cancel their timeouts.
- Sources and combined signal are linked through weak references, but a non-aborted combined signal stays alive while it has source signals and registered abort listeners (or internal abort steps registered by an API). Remove abort listeners you add to the combined signal when the operation finishes.
- MDN marks `AbortSignal.any()` Baseline widely available (since March 2024) and available in Web Workers.

Self-check: `AbortSignal.any` aborts the fetch when either the cancel button or the timeout fires.

## Checked

Confirmed against MDN "AbortSignal: any() static method" (page last modified 2026-09-01), read 2026-11-08. Removed: Node version claim, `signal.reason.name` and `throwIfAborted()` advice, the `setTimeout` fallback and "new controller per attempt" remark (not on the page).
Method: docs-only read of cited pages, 2026-11-08
