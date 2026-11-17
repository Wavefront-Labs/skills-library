---
id: computing-software.software-engineering.javascript.js-user-timing-marks
name: js-user-timing-marks
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, performance-mark-measure, js-performance]
level: practitioner
status: docs-checked
description: "Create named measures with performance.measure: mark names or measureOptions start, end, duration and detail, error cases, and the DevTools extensibility detail."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/Performance/measure"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# User Timing measures with performance.measure()

- `performance.measure(name, startMark, endMark)` creates a `PerformanceMeasure` between two named `PerformanceMark` entries and returns it; read `.duration` from the result. Marks are referred to by string name. The method is available in Web Workers.
- Forms: `measure(name)`, `measure(name, startMark)`, `measure(name, startMark, endMark)`, `measure(name, measureOptions)`, `measure(name, measureOptions, endMark)`. With only a name, start is 0 and end is `performance.now()`.
- `measureOptions` can hold `start` and `end` (a `DOMHighResTimeStamp` or a mark name), `duration` (ms) and `detail` (any structured-cloneable metadata, default null). Example: `performance.measure("login-click", { start: myClickEvent.timeStamp, end: myMarker.startTime })`.
- To give only an end mark, pass an empty options object: `performance.measure("m", {}, "myEndMarker")`.
- If `start` is omitted, startTime comes from the end and duration if given, else 0. If `end` is omitted, it is derived from start and duration, else `performance.now()`.
- Errors: `TypeError` when start, end or duration are ambiguous (both `endMark` and `measureOptions`; `duration` without `start` or `end`; all of `start`, `end` and `duration`). `SyntaxError` DOMException when a named mark does not exist in the buffer. `DataCloneError` when `detail` cannot be structured-cloned.
- Some browsers support the DevTools Extensibility API: put a `devtools` object inside `detail` (`dataType: "track-entry"` or `"marker"`, `track`, `trackGroup`, `color`, `properties`, `tooltipText`) to show the entry on a custom track in performance traces. `track` and `trackGroup` are required for `track-entry`. See Chrome's Extensibility API documentation for details.

Self-check: calling `measure` with a mark name that was never created throws a `SyntaxError`, and the returned measure has `entryType` of `"measure"`.

## Checked

Confirmed on the MDN Performance.measure() page (modified September 2026): all points above. Removed: `performance.mark` options, `getEntriesByName`, `PerformanceObserver`, `clearMarks`, the `performance.now()` versus `Date.now()` comparison, Node `perf_hooks` and the "Timings track" self-check, none of which this page states (the page only says the devtools detail surfaces entries in custom tracks).

Method: docs-only read of cited pages, 2026-11-08
