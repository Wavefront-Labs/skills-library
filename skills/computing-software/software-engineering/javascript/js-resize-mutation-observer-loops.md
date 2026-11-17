---
id: computing-software.software-engineering.javascript.js-resize-mutation-observer-loops
name: js-resize-mutation-observer-loops
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, resizeobserver-loop, js-observers]
level: advanced
status: docs-checked
description: "Avoid ResizeObserver loop errors with an expected-size guard or requestAnimationFrame, and set MutationObserver.observe options precisely."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/ResizeObserver", "https://developer.mozilla.org/en-US/docs/Web/API/ResizeObserverEntry", "https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver/observe", "https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ResizeObserver and MutationObserver pitfalls

- "ResizeObserver loop completed with undelivered notifications." appears when a callback resizes observed elements so that new resize notifications keep arriving. MDN notes the message only prevents user-agent lockup, not the loop itself.
- If you do not intend an infinite loop, make the resize code not retrigger the callback, for example by tracking an "expected size" and skipping the write when the size already matches. If you do intend it, defer the resizing into a `requestAnimationFrame` callback.
- Without handling, observers may settle on a stable layout, but visitors can see a flash of broken layout because changes spread across several frames.
- `entry.contentBoxSize` is an array of objects in modern browsers (to report fragmented elements, such as multi-column), so read `entry.contentBoxSize[0].inlineSize`; `contentRect` is the older fallback. Old Firefox returned a single object rather than an array.
- `MutationObserver.observe(node, { childList: true, subtree: true, attributes: true, attributeFilter: ["class"] })`: at least one of `childList`, `attributes`, `characterData` must be true or `observe()` throws a `TypeError`. Setting `attributeFilter` implies `attributes` defaults to true. Narrow the options to the changes you need.
- Do not mutate the observed subtree from the callback in a way that retriggers it without a guard. `takeRecords()` returns pending records; `disconnect()` on cleanup.

Self-check: an observer on a resizing panel logs steady sizes with no loop message in the console.

## Checked

2026-11-03. Confirmed on MDN: ResizeObserver (loop message, lockup note, flash-of-layout note, expected-size and requestAnimationFrame fixes), ResizeObserverEntry (contentBoxSize array, contentRect, old Firefox behaviour), MutationObserver.observe (options, defaults, TypeError conditions), MutationObserver (takeRecords, disconnect). Removed: "use contentBoxSize for accuracy" as a general claim, reworded to the documented array form, and the microtask-batching claim.
Method: documentation only; no commands were run.
