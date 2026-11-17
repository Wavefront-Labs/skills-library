---
id: computing-software.web-development.web-performance.performanceobserver-and-user-timing
name: performanceobserver-and-user-timing
category: computing-software
field: web-development
product: web-performance
tags: [performance-measurement, performanceobserver, user-timing, rum, web-vitals, server-timing]
level: practitioner
status: verified
description: "Instrumenting custom performance metrics with User Timing marks/measures and PerformanceObserver, collecting Core Web Vitals and resource timing in RUM, and Server-Timing headers."
sources:
  - https://developer.chrome.com/docs/devtools/performance/extension
  - https://developer.mozilla.org/en-US/docs/Web/API/Performance_API/User_timing
  - https://developer.mozilla.org/en-US/docs/Web/API/PerformanceObserver
  - https://github.com/GoogleChrome/web-vitals
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Server-Timing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PerformanceObserver and User Timing

## 1. Custom milestones
```js
performance.mark("search:start");
await runSearch(q);
performance.mark("search:end");
const m = performance.measure("search", { start: "search:start", end: "search:end", detail: { q: q.length } });
send({ name: m.name, duration: m.duration });
```
Marks/measures appear in the DevTools Performance panel "Timings" track - great for correlating with traces. DevTools extensibility: `performance.measure(name, { detail: { devtools: { track: "My app", color: "primary" } } })` creates custom tracks (a Chromium DevTools feature; see the Chrome DevTools performance extensibility docs for fields and version; the `detail` object round-trips on the returned measure, run).

## 2. Observe entries
```js
const po = new PerformanceObserver(list => {
  for (const e of list.getEntries()) {
    if (e.entryType === "resource" && e.duration > 1000) send({ slowResource: e.name, dur: e.duration, size: e.transferSize });
  }
});
po.observe({ type: "resource", buffered: true });   // buffered: include entries before observing
```
Types: `navigation`, `resource`, `paint`, `largest-contentful-paint`, `layout-shift`, `event` (interaction timing), `long-animation-frame`, `mark`, `measure`, `element` (Element Timing via `elementtiming` attribute). `PerformanceObserver.supportedEntryTypes` to feature-detect (a Chromium run listed: element, event, first-input, largest-contentful-paint, layout-shift, long-animation-frame, longtask, mark, measure, navigation, paint, resource, soft-navigation, visibility-state, interaction-contentful-paint; per MDN compat data `layout-shift`, `long-animation-frame` and `element` entries are not available in Firefox or Safari).

## 3. Core Web Vitals in RUM
Use the `web-vitals` library rather than hand-rolling (handles bfcache restores, prerender, visibility, final values):
```js
import { onLCP, onINP, onCLS, onTTFB } from "web-vitals/attribution";
const send = m => navigator.sendBeacon("/rum", JSON.stringify({ name: m.name, value: m.value, rating: m.rating, id: m.id, nav: m.navigationType, attr: m.attribution }));
onLCP(send); onINP(send); onCLS(send); onTTFB(send);
```
Report p75 per page template and device class.

## 4. Server-Timing
```
Server-Timing: db;dur=53;desc="orders query", cache;desc="miss", app;dur=120
```
Visible in DevTools Timing tab and exposed (run: `db`, `cache` and `app` parsed with `duration` and `description`) via `performance.getEntriesByType("navigation")[0].serverTiming` (cross-origin needs `Timing-Allow-Origin`). Don't expose sensitive internals publicly.

## 5. Caveats
- Resource timing sizes are 0 for cross-origin resources without `Timing-Allow-Origin` (run: `transferSize` 0 without the header, 316 with it).
- The resource timing buffer holds 250 entries by default (run in Chromium: 300 same-origin fetches left exactly 250 entries); later ones are dropped unless you raise it with `performance.setResourceTimingBufferSize`. Entries for fetches arrive asynchronously, so read them after a short delay or via an observer.
- Clear marks you no longer need in SPAs (`performance.clearMarks`).

## Verify
Custom measures show in the DevTools Timings track; RUM dashboard receives CWV with attribution; Server-Timing appears in the Network panel.
