---
id: computing-software.software-engineering.javascript.js-intersection-resize-mutation-observers
name: js-intersection-resize-mutation-observers
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-observers, intersectionobserver, resizeobserver, mutationobserver, lazy-loading]
level: practitioner
status: docs-checked
description: "Choose between IntersectionObserver, ResizeObserver and MutationObserver, and clean them up with unobserve, disconnect and takeRecords."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API", "https://developer.mozilla.org/en-US/docs/Web/API/ResizeObserver", "https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver", "https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver/observe"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Observers

- `IntersectionObserver(cb, { root, rootMargin, threshold })` asynchronously reports how much of a target is visible inside an ancestor or the viewport. Use it for lazy loading and similar visibility checks; `unobserve(target)` once done and `disconnect()` on teardown.
- `ResizeObserver` reports changes to an element's content or border box, or an SVG element's bounding box (`contentBoxSize`, `contentRect`). `unobserve()` and `disconnect()` stop it. Changing layout inside the callback can trigger the console error "ResizeObserver loop completed with undelivered notifications"; the fix is covered in js-resize-mutation-observer-loops.
- `MutationObserver` watches DOM changes. `observe(node, options)` needs at least one of `childList`, `attributes` or `characterData` true, otherwise it throws a `TypeError`; `subtree: true` extends watching to descendants. `takeRecords()` returns pending records and `disconnect()` stops all callbacks.

## Checked

2026-11-03. Confirmed on MDN: Intersection Observer API, ResizeObserver (what it reports, loop message, unobserve/disconnect), MutationObserver and MutationObserver.observe (required options, TypeError, subtree, takeRecords, disconnect). Removed: the claims that mutation callbacks are batched as microtasks, that observers behave differently in hidden tabs from timers, and the `loading="lazy"` preference (kept in js-intersection-observer-lazyload); also the ECMAScript and MDN JavaScript root sources, which do not cover these APIs.
Method: documentation only; no commands were run.
