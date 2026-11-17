---
id: computing-software.software-engineering.javascript.js-dom-events-and-delegation
name: js-dom-events-and-delegation
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-dom-events, event-delegation, addeventlistener, passive-listeners, event-bubbling]
level: practitioner
status: docs-checked
description: "Handle DOM events with addEventListener options, propagation control, closest-based delegation, passive listeners and CustomEvent."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener", "https://developer.mozilla.org/en-US/docs/Web/API/Event/stopPropagation", "https://developer.mozilla.org/en-US/docs/Web/API/Event/stopImmediatePropagation", "https://developer.mozilla.org/en-US/docs/Web/API/Event/preventDefault", "https://developer.mozilla.org/en-US/docs/Web/API/Event/currentTarget", "https://developer.mozilla.org/en-US/docs/Web/API/CustomEvent", "https://developer.mozilla.org/en-US/docs/Web/API/Element/closest"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DOM events

- `el.addEventListener(type, handler, { once, passive, capture, signal })`. `once: true` removes the listener after one call; `signal` removes it when the owning `AbortController` aborts, so one `abort()` can remove many listeners.
- Propagation: capture runs from Window down to the target's parent, then the target, then bubbling back up (only if `bubbles` is true). `stopPropagation()` stops further travel but not other listeners on the same element; `stopImmediatePropagation()` also stops those. `preventDefault()` cancels the default action; it has no effect on a non-cancelable event.
- Delegation: attach one listener to a parent and use `event.target.closest(".item")` (returns the nearest matching ancestor-or-self, or `null`); it works for children added later.
- `event.target` is the origin; `event.currentTarget` is the element the listener is attached to.
- Passive: `passive: true` promises never to call `preventDefault()`, and a call is ignored with a possible console warning. It defaults to `true` for `wheel`, `mousewheel`, `touchstart` and `touchmove` on Window, Document, `documentElement` and `body`; to override, set `passive: false` explicitly, and only when you must cancel.
- Custom events: `el.dispatchEvent(new CustomEvent("x", { detail, bubbles: true }))`. `Event` options `bubbles` and `cancelable` default to false; `preventDefault()` on a dispatched event needs `cancelable: true`.

## Checked

2026-11-03. Confirmed on MDN: EventTarget.addEventListener (options, once, signal, passive defaults), Event.stopPropagation, stopImmediatePropagation, preventDefault, eventPhase, Element.closest, CustomEvent (`detail`), Event constructor (`bubbles`, `cancelable`, `composed` defaults). Removed: which events do not bubble (`focus`, `blur`, `mouseenter`) and the `focusin`/`focusout`/`mouseover` substitutes, the pointer-events preference, and the "same function reference" note for `removeEventListener`; none was verified on a page read. Corrected the passive default list, which was only "touchstart/wheel".
Method: documentation only; no commands were run.
