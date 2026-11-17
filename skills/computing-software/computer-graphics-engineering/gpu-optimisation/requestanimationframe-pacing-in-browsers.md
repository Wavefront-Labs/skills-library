---
id: computing-software.computer-graphics-engineering.gpu-optimisation.requestanimationframe-pacing-in-browsers
name: requestanimationframe-pacing-in-browsers
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, frame-pacing, requestanimationframe, web-rendering, frame-timing, jank, webgl, webgpu]
level: practitioner
status: docs-checked
description: "Pace web rendering with requestAnimationFrame: timestamp-based updates, high-refresh displays, background throttling, no setTimeout loops, diagnosing jank."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame", "https://html.spec.whatwg.org/multipage/imagebitmap-and-animations.html#animation-frames", "https://web.dev/articles/rendering-performance"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# requestAnimationFrame pacing in browsers

## 1. Basic loop
```js
let last = 0;
function frame(t) {                      // t: DOMHighResTimeStamp (ms), same for every callback in a frame
  const dt = Math.min((t - last) / 1000, 0.1);   // clamp after tab switches
  last = t;
  update(dt);
  render();
  requestAnimationFrame(frame);
}
requestAnimationFrame(t => { last = t; requestAnimationFrame(frame); });
```
- Callback frequency generally matches the display refresh rate (60, 75, 120, 144 Hz are common); never assume
  60 Hz - MDN warns animations not scaled by the timestamp run faster on high-refresh screens.
- Use the callback's timestamp for per-frame progress; `performance.now()` is an alternative with little extra precision.

## 2. Fixed-step simulation
For deterministic physics, accumulate time and step at a fixed rate; render with interpolation:
```js
acc += dt; while (acc >= STEP) { simulate(STEP); acc -= STEP; } render(acc / STEP);
```

## 3. Throttling and visibility
- rAF calls are paused in most browsers in background tabs and hidden iframes; clamp dt on resume.

## 4. Anti-patterns
- `setTimeout`/`setInterval` loops: not vsync-aligned, cause judder and wasted frames.
- Doing heavy work in rAF that exceeds the frame budget (the frame period at the display's refresh rate): split work across frames or move it off the main thread.

## 5. Diagnosing jank
Use the browser's performance profiler for dropped frames and long main-thread tasks (web.dev rendering performance guide). Measure the frame time distribution in-app (rolling histogram of `dt`) and show percentiles in a debug overlay.

## Gotchas
- Animations tied to frames (not time) run faster on high-refresh monitors.

## Checked
2026-11-01. Confirmed on MDN requestAnimationFrame: callback rate matches display refresh, rAF paused in background tabs and hidden iframes, use of the timestamp argument, shared timestamp within a frame, performance.now() alternative. Removed: 1 Hz and 30 Hz throttling figures, WebXR note, readback and canvas-resize claims, OffscreenCanvas advice, DevTools panel names (not in fetched pages).
Method: documentation only; no commands were run.

## Verify
- [ ] Animation speed identical at 60 Hz and 120 Hz.
- [ ] No long tasks > frame budget in a profiler trace of typical interaction.
