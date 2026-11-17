---
id: computing-software.software-engineering.javascript.js-raf-animation-loop
name: js-raf-animation-loop
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, requestanimationframe-loop, js-timers]
level: practitioner
status: docs-checked
description: "Drive animation with requestAnimationFrame using the callback timestamp, re-request each frame, cancel by id, and avoid 0 as a sentinel."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# requestAnimationFrame loops and timing

- `requestAnimationFrame(callback)` asks the browser to call `callback` before the next repaint. Calls generally match the display refresh rate (60, 75, 120, 144 Hz and others). It is one-shot: the callback must call `requestAnimationFrame()` again to animate another frame.
- The callback receives a `DOMHighResTimeStamp` (milliseconds, the end time of the previous frame's rendering). Always compute progress from it (or another clock), otherwise the animation runs faster on high-refresh screens. Callbacks that fire in the same frame all receive the same timestamp.
- Pattern from MDN: record `start` on the first callback, compute `elapsed = timestamp - start`, derive the position from `elapsed`, and request another frame only until the end condition is met.
- If you need a zero point before the first frame, `document.timeline.currentTime` aligns with the timestamp argument. `performance.now()` also works, but MDN notes it does not let you synchronise callbacks reliably. Some browsers delay the first callback by several frames, so setting zero in the first callback is recommended when you do not need to sync to an external clock.
- `requestAnimationFrame()` returns a request ID; pass it to `cancelAnimationFrame()` to cancel. Do not assume anything about its value, and do not use `0` as an "invalid" sentinel because the counter may wrap around; use `null` instead.
- Calls are paused in most browsers in background tabs and hidden iframes.

Self-check: the animation covers the same distance in the same elapsed time at 60 Hz and 144 Hz.

## Checked

Confirmed on the MDN requestAnimationFrame page: one-shot behaviour, timestamp semantics and warning, zero-point options, request ID rules and the background-tab pause. Removed: the "timers throttled to about 1 s" figure, layout read/write ordering, the 16.7 ms work budget advice, off-main-thread CSS and Web Animations claims and the `prefers-reduced-motion` advice, none of which the page states.

Method: docs-only read of cited pages, 2026-11-08
