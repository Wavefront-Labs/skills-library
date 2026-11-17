---
id: computing-software.web-development.frontend-development.pointer-events-and-capture
name: pointer-events-and-capture
category: computing-software
field: web-development
product: frontend-development
tags: [pointer-events, setpointercapture, touch-action, drag-gestures, coalesced-events, dom-events]
level: practitioner
status: docs-checked
description: "Unified mouse/touch/pen handling with Pointer Events: drag with setPointerCapture, touch-action, pointercancel, multi-touch, coalesced events and compat mouse events."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Pointer_events
  - https://developer.mozilla.org/en-US/docs/Web/API/Element/setPointerCapture
  - https://developer.mozilla.org/en-US/docs/Web/CSS/touch-action
  - https://www.w3.org/TR/pointerevents/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pointer events and pointer capture

## 1. One API for mouse, touch, pen
`pointerdown / pointermove / pointerup / pointercancel` with `e.pointerType` (`"mouse" | "pen" | "touch"`), `e.pointerId`, `e.isPrimary`, `e.pressure`, `e.width/height`. Use these instead of separate mouse + touch handlers.

## 2. Draggable element
```js
handle.addEventListener("pointerdown", e => {
  if (e.button !== 0) return;
  handle.setPointerCapture(e.pointerId);   // keep receiving moves even outside the element
  const startX = e.clientX - x;
  const move = ev => { x = ev.clientX - startX; el.style.translate = `${x}px 0`; };
  const end = () => { handle.removeEventListener("pointermove", move); };
  handle.addEventListener("pointermove", move);
  handle.addEventListener("lostpointercapture", end, { once: true }); // fires on up AND cancel
});
```
```css
.handle { touch-action: none; }   /* else the browser scrolls and fires pointercancel */
```
`touch-action: pan-y` allows vertical panning while you handle horizontal swipes. By default the browser handles panning and pinching and sends `pointercancel`.

## 3. pointercancel
Fired when the browser takes over (for example a pan or pinch gesture starts). Always revert drag state on cancel. Pointer capture is released implicitly after `pointerup` and `pointercancel`, so `lostpointercapture` covers both.

## 4. Drawing and precision
```js
canvas.addEventListener("pointermove", e => {
  for (const p of e.getCoalescedEvents?.() ?? [e]) drawPoint(p.offsetX, p.offsetY, p.pressure);
});
```
Coalesced events give the full-rate samples between frames; `getPredictedEvents()` reduces perceived latency.

## 5. Multi-touch
Track active pointers in a `Map` by `pointerId` for pinch/rotate; compute distance between the two entries.

## Gotchas
- Compatibility mouse events (`mousedown`, `mouseup`) follow pointer events; cancelling `pointerdown` suppresses them for that pointer type, but `click`, `auxclick` and `contextmenu` are always dispatched.
- Capture targets the element: `e.target` of captured moves is the capturing element, not what is under the finger (use `document.elementFromPoint`).
- Provide a single-pointer alternative for every drag (WCAG 2.5.7 Dragging Movements).

## Verify
- [ ] Drag works with mouse, touch (DevTools device mode and a real phone) and pen; page does not scroll during drag.
- [ ] Dragging off the element and releasing ends the drag.

## Checked

Checked 2026-10-26 against the W3C Pointer Events specification source (w3c/pointerevents), mdn/content (main) setPointerCapture, getCoalescedEvents and touch-action pages, mdn/browser-compat-data and the WCAG 2.2 Dragging Movements understanding document.

- Confirmed: capture is released implicitly on `pointerup` and `pointercancel` and `lostpointercapture` follows; cancelling `pointerdown` sets the prevent-mouse-event flag but `click`, `auxclick` and `contextmenu` are still dispatched; `touch-action` stops browser panning and the `pointercancel` it causes; `getCoalescedEvents()` (Safari 18.2) and `getPredictedEvents()`; WCAG 2.5.7 requires a single-pointer alternative.
- Reworded: the compatibility mouse events note, to name the events the specification lists.

Method: documentation only; no commands were run.
