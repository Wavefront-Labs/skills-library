---
id: computing-software.web-development.web-performance.debounce-and-throttle-input-handlers
name: debounce-and-throttle-input-handlers
category: computing-software
field: web-development
product: web-performance
tags: [inp, debounce, throttle, event-handlers, requestanimationframe, javascript, debounce-function, throttle-function]
level: practitioner
status: verified
description: "Debouncing and throttling input, scroll and resize handlers to protect responsiveness: correct implementations, rAF throttling, leading/trailing edges, and when not to."
sources:
  - https://web.dev/articles/optimize-inp
  - https://developer.mozilla.org/en-US/docs/Glossary/Debounce
  - https://developer.mozilla.org/en-US/docs/Glossary/Throttle
  - https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Debouncing and throttling input handlers

## 1. Choose
- **Debounce**: run once after input stops for N ms - search-as-you-type requests, autosave, validation, resize-driven expensive recalcs.
- **Throttle**: run at most once per N ms during continuous input - scroll position tracking, drag analytics, infinite-scroll checks.
- **rAF throttle**: at most once per frame - visual updates driven by pointer/scroll.

## 2. Implementations
```js
function debounce(fn, ms) {
  let t, pending;
  const d = (...a) => { pending = a; clearTimeout(t); t = setTimeout(() => { const p = pending; pending = undefined; fn(...p); }, ms); };
  d.cancel = () => { clearTimeout(t); pending = undefined; };
  d.flush = () => { if (pending) { clearTimeout(t); const p = pending; pending = undefined; fn(...p); } };  // run now, only if a call is waiting
  return d;
}
function throttle(fn, ms) {
  let last = -Infinity, t;
  return (...a) => {
    const now = performance.now(), wait = ms - (now - last);
    clearTimeout(t);                       // drop the older trailing call; without this it fires with stale args
    if (wait <= 0) { last = now; fn(...a); }
    else t = setTimeout(() => { last = performance.now(); fn(...a); }, wait);   // trailing call, newest args
  };
}
function rafThrottle(fn) {
  let queued = false, args;
  return (...a) => { args = a; if (!queued) { queued = true; requestAnimationFrame(() => { queued = false; fn(...args); }); } };
}
```
Lodash `debounce`/`throttle` support `leading`, `trailing`, `maxWait` and expose `cancel` and `flush`. Run on Node 20: the first draft of this throttle (no `clearTimeout` on the leading branch) fired a stale trailing call at the same instant as the leading one, so values arrived out of order (15 then 14); the version above fires 0, 3, 7, 10, ... about every 108 ms for events every 20 ms with a 100 ms limit, each with the newest value.

## 3. Keep the immediate feedback
Debounce the **expensive** part, not the visible echo: the input value updates instantly (native), filtering 10,000 items runs debounced (~150-300 ms). Better still, make the work cheap or move it to a worker; debouncing only hides the cost until the user pauses.

## 4. Gotchas
- Debounced handlers in components must be created once (memoised) and cancelled on unmount, else stale closures and calls after unmount.
- Abort stale fetches (AbortController) - debounce doesn't prevent out-of-order responses.
- Don't debounce clicks/submit for "double-submit prevention" - disable the button or make the action idempotent.
- Passive listeners for scroll/touch (`{ passive: true }`) avoid blocking scrolling regardless of throttling.
- Prefer `IntersectionObserver`/`ResizeObserver` over throttled scroll/resize polling.
- React: `useDeferredValue` / `startTransition` may replace debounce for rendering-heavy updates.

## Verify
Performance trace while typing fast shows one heavy task after pausing instead of one per keystroke; INP for typing interactions under 200 ms on a throttled CPU.
