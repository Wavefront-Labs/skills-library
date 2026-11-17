---
id: computing-software.web-development.frontend-development.customevent-and-eventtarget-messaging
name: customevent-and-eventtarget-messaging
category: computing-software
field: web-development
product: frontend-development
tags: [dom-manipulation, customevent, eventtarget, events, web-components, pub-sub]
level: practitioner
status: docs-checked
description: "Using CustomEvent and EventTarget for decoupled component messaging: detail payloads, bubbles and composed for shadow DOM, typed event buses, and cleanup."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/CustomEvent
  - https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/dispatchEvent
  - https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/EventTarget
  - https://developer.mozilla.org/en-US/docs/Web/API/Event/composed
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CustomEvent and EventTarget messaging

## 1. Emit from a component
```js
this.dispatchEvent(new CustomEvent("cart:add", {
  detail: { sku, qty },     // payload; treat as read-only
  bubbles: true,            // let ancestors listen (delegation)
  composed: true,           // cross shadow DOM boundaries
  cancelable: true,         // allow listeners to veto
}));
```
`dispatchEvent` returns `false` if a listener called `preventDefault()` - use for "before" events:
```js
if (!el.dispatchEvent(new CustomEvent("tab:beforechange", { cancelable: true, detail }))) return;
```

## 2. Listen
```js
const ac = new AbortController();
document.addEventListener("cart:add", e => update(e.detail), { signal: ac.signal });
// teardown: ac.abort()
```

## 3. Standalone bus (no DOM needed)
```js
class Bus extends EventTarget {
  emit(type, detail) { this.dispatchEvent(new CustomEvent(type, { detail })); }
  on(type, fn, opts) { const h = e => fn(e.detail); this.addEventListener(type, h, opts); return () => this.removeEventListener(type, h); }
}
export const bus = new Bus();
```
`EventTarget` has a constructor, so a plain class can extend it.

## 4. Rules
- Name events in a namespace (`cart:add`, `my-tabs-change`) - avoid colliding with native names (`change`, `select`).
- `dispatchEvent` is **synchronous**: listeners run before it returns, unlike native events the browser queues as tasks.
- Without `composed: true`, events from inside a shadow root stop at the host; with it, `event.target` is retargeted to the host outside.
- Native events bubble through the DOM tree.
- Prefer events for "something happened" (child to parent), properties/attributes for "here is data" (parent to child).

## Verify
Test with a listener spy: event fires once with expected detail; `preventDefault` cancels the action; listeners removed after abort.

## Checked

2026-10-26. MDN dispatchEvent (synchronous; returns false if a cancelable event was cancelled with preventDefault), EventTarget constructor and Event.composed (crossing the shadow DOM boundary). Removed the unconfirmed Node 15 version, TypeScript, listener-exception and React portal statements.

Method: documentation only; no commands were run.
