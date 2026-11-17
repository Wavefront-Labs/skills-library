---
id: computing-software.software-engineering.javascript.js-passive-listeners-custom-events
name: js-passive-listeners-custom-events
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, passive-listeners, js-dom-events]
level: practitioner
status: docs-checked
description: "Use the passive, once and signal listener options and dispatch CustomEvent with detail, bubbles and composed."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener", "https://developer.mozilla.org/en-US/docs/Web/API/CustomEvent", "https://developer.mozilla.org/en-US/docs/Web/API/Event/Event", "https://developer.mozilla.org/en-US/docs/Web/API/Event/preventDefault"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Passive listeners and CustomEvent

- `{ passive: true }` declares the listener never calls `preventDefault()`, so the browser can start the default action (such as scrolling) without waiting. If a passive listener does call it, nothing happens and a console warning may appear.
- The default is `true` for `wheel`, `mousewheel`, `touchstart` and `touchmove` on Window, Document, `documentElement` and `body`, and `false` elsewhere; set `false` explicitly to override. The plain `scroll` event cannot be cancelled, so `passive` does not matter for it.
- `{ once: true }` removes the listener after it runs; `{ signal }` removes it when the `AbortController` that owns the signal calls `abort()`.
- `el.dispatchEvent(new CustomEvent("cart:add", { detail: { id }, bubbles: true, composed: true }))`: `detail` carries the payload (`CustomEvent.detail`), `bubbles` defaults to false, and `composed` (default false) decides whether listeners outside a shadow root are triggered.
- `preventDefault()` on an event dispatched with `dispatchEvent()` has no effect unless it was created with `cancelable: true`.

## Checked

2026-11-03. Confirmed on MDN: EventTarget.addEventListener (passive, once, signal, default passive targets, scroll note), CustomEvent (`detail`), Event constructor (`bubbles`, `cancelable`, `composed` defaults), Event.preventDefault (passive and non-cancelable behaviour). Removed: the `class Bus extends EventTarget` pattern, the `requestAnimationFrame` throttling advice for `scroll`/`pointermove`/`resize`, and the Performance-panel jank check (not on pages read).
Method: documentation only; no commands were run.
