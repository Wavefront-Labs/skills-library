---
id: computing-software.software-engineering.javascript.js-timers-animation-frames-and-scheduling
name: js-timers-animation-frames-and-scheduling
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-timers, settimeout, setinterval, requestanimationframe, debounce-throttle]
level: practitioner
status: docs-checked
description: "Schedule work with timers, requestAnimationFrame and idle callbacks; implement debounce and throttle."
sources: ["https://tc39.es/ecma262/", "https://developer.mozilla.org/en-US/docs/Web/JavaScript"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timers and scheduling

- `setTimeout(fn, ms)` returns an id for `clearTimeout`; `setInterval` can stack if the callback outlasts the interval, so prefer a self-rescheduling `setTimeout`. Extra arguments pass through: `setTimeout(fn, 0, a, b)`.
- Timers run late: browsers enforce a minimum of 4 ms once a timer is nested 5 times, and inactive tabs get a minimum delay (browser-dependent; about 1 s in Firefox desktop and Chrome); never use them for exact timing, compare `performance.now()` or `Date.now()` deltas.
- `requestAnimationFrame` runs before the next paint (generally matches the display refresh rate, commonly 60 Hz; paused in background tabs); use it for visual updates and cancel with `cancelAnimationFrame`.
- `requestIdleCallback(fn, { timeout })` for non-urgent work (not Baseline per MDN, so feature-detect; a `timeout` is strongly recommended for required work).
- Debounce: reset a timer on each call and run after quiet (search-as-you-type); throttle: run at most once per interval (`scroll`, `resize`). Clear timers on teardown.
- `await new Promise(r => setTimeout(r, ms))` as sleep; add an AbortSignal for cancellation.

## Checked

2026-11-02. Checked against MDN Window.setTimeout (extra arguments, nested-timer 4 ms minimum after 5 levels, inactive-tab throttling), requestAnimationFrame (before next repaint, refresh-rate matched, paused in background) and requestIdleCallback (not Baseline, timeout option). Removed: the Safari-specific support claim and the fixed 60 Hz figure.

Method: documentation only; no commands were run.
