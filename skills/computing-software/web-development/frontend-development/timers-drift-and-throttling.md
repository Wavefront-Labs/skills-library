---
id: computing-software.web-development.frontend-development.timers-drift-and-throttling
name: timers-drift-and-throttling
category: computing-software
field: web-development
product: frontend-development
tags: [settimeout-drift, timer-throttling, setinterval, background-tabs, timers, javascript]
level: practitioner
status: docs-checked
description: "How setTimeout/setInterval really behave: minimum delays, drift, background-tab and intensive throttling, the 24.8-day overflow, and drift-correcting timers."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Window/setTimeout
  - https://developer.mozilla.org/en-US/docs/Web/API/Scheduler/yield
  - https://nodejs.org/api/timers.html
  - https://github.com/mdn/browser-compat-data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timers: drift and throttling

## 1. A delay is a minimum, not a schedule
- Callbacks run only when the main thread is free; a 200 ms long task delays every due timer.
- Once a nested `setTimeout` has been scheduled 5 times, browsers enforce a minimum of 4 ms.
- `setInterval` ticks are late by however long the thread was busy, so counting ticks does not measure elapsed time.

## 2. Throttling in hidden tabs
- Inactive tabs: browsers enforce a minimum delay; Firefox Desktop uses 1 second and Chrome checks throttled timers once per second.
- Chrome intensive throttling (Chrome 88+): page hidden for more than 5 minutes, silent for more than 30 seconds, nesting count 5 or higher, no active WebRTC: timers checked once per minute.
- Firefox for Android has a 15-minute minimum for inactive tabs and may unload them.
Consequence: countdowns, polling and session-timeout logic computed by counting ticks is wrong. Compute from timestamps.

## 3. Drift-correcting timer
```js
function every(ms, fn, signal) {
  const start = performance.now(); let n = 0;
  (function tick() {
    if (signal?.aborted) return;
    fn();
    const next = start + ++n * ms;
    setTimeout(tick, Math.max(0, next - performance.now()));
  })();
}
```
For wall-clock displays, recompute remaining time from `Date.now()` on every tick and on `visibilitychange`.

## 4. Right tool
| Need | Use |
|---|---|
| visual updates | `requestAnimationFrame` |
| run after current task | `queueMicrotask` / `setTimeout(fn, 0)` |
| yield during long work | `scheduler.yield()` (Chrome 129, Firefox 142, not Safari) with a `setTimeout` fallback |
| background work | Web Worker; Push or Background Sync for work while the page is closed |

## 5. Edge cases
- Delays above 2147483647 ms (about 24.8 days) overflow (a signed 32-bit integer); chain shorter timers.
- Node: `timers/promises` provides promise-based timers; see the Node timers documentation for `unref()`.
- Always clear timers on unmount/teardown to avoid callbacks on dead components.

## Verify
- [ ] Hide the tab for 6 minutes; countdown still shows correct remaining time on return.

## Checked

2026-10-26. MDN setTimeout (4 ms minimum after 5 nested calls; maximum delay 2147483647 ms; inactive-tab throttling for Firefox and Chrome, including intensive throttling since Chrome 88 with its once-per-minute rule) and browser-compat-data for scheduler.yield (Chrome 129, Firefox 142). Removed the unconfirmed Page Lifecycle freeze, rAF-paused, Worker-throttling, interval-drop and Node unref statements.

Method: documentation only; no commands were run.
