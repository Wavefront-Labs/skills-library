---
id: computing-software.software-engineering.javascript.js-debounce-throttle
name: js-debounce-throttle
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, debounce-throttle, js-timers]
level: practitioner
status: docs-checked
description: "Implement debounce with setTimeout/clearTimeout and know the timer limits: 4 ms nested clamp, 2147483647 ms maximum delay and background-tab throttling."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/Window/setTimeout"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debounce, throttle and timer limits

- Debounce (wait for quiet): `const d = (fn, ms) => { let t; return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); }; };` Use it for search-as-you-type and resize. `setTimeout()` returns a timeout ID that `clearTimeout()` cancels before it fires.
- Throttle (at most once per interval): track the time of the last run and skip calls inside the interval. Decide deliberately whether the leading call, the trailing call or both should run.
- Repeated work: MDN points to `setInterval()` for calling a function repeatedly; whichever you use, clear the timer on teardown.

## Timer limits (MDN, setTimeout)
- The `delay` is converted to a signed 32-bit integer, so the maximum is 2147483647 ms (about 24.8 days); larger values overflow. In Node.js a larger timeout runs immediately.
- Per the HTML standard, browsers enforce a minimum timeout of 4 ms once a nested `setTimeout` has been scheduled 5 times.
- Inactive tabs: browsers enforce a minimum delay and the details differ by browser. Firefox Desktop uses 1 second for inactive tabs. Chrome throttles to once per second in some states and applies "intensive throttling" (checked once per minute, from Chrome 88) when nesting count is 5 or higher, the page has been invisible for more than 5 minutes and silent for more than 30 seconds, and WebRTC is inactive.
- So a timer callback can run later than requested; do not use timers to measure elapsed time, read the clock instead.

## Self-check
A debounced handler fires once after rapid input stops.

## Checked
Confirmed on the MDN setTimeout page: clearTimeout and timeout IDs, 32-bit maximum delay and Node behaviour, 4 ms nested minimum, background-tab throttling in Firefox and Chrome.
Removed: the claim that `setInterval` drifts and the self-rescheduling advice, the "background tabs throttle to 1 s" generalisation (browser-dependent), requestAnimationFrame and lodash mentions.
Method: docs-only read of cited pages, 2026-11-08
