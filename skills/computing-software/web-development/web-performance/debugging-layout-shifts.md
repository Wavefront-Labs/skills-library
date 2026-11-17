---
id: computing-software.web-development.web-performance.debugging-layout-shifts
name: debugging-layout-shifts
category: computing-software
field: web-development
product: web-performance
tags: [layout-instability-api, cls-debugging, layout-shift-culprits, cls-attribution, core-web-vitals, performance]
level: practitioner
status: docs-checked
description: "Finding what causes CLS: Layout Instability API entries and sources, session windows, DevTools layout shift culprits, web-vitals attribution, and lab vs field differences."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/LayoutShift
  - https://web.dev/articles/debug-layout-shifts
  - https://github.com/GoogleChrome/web-vitals#attribution
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging layout shifts

## 1. How CLS is computed
Each unexpected shift scores impact fraction x distance fraction. Shifts are grouped into **session windows** (less than 1 s between shifts, 5 s maximum per window); CLS is the worst window over the page's lifetime. Shifts within 500 ms of a user input (`hadRecentInput`) are excluded.

## 2. See shifts live
```js
new PerformanceObserver(list => {
  for (const e of list.getEntries()) {
    if (e.hadRecentInput) continue;
    console.log(e.value.toFixed(4), e.sources.map(s => [s.node, s.previousRect, s.currentRect]));
  }
}).observe({ type: "layout-shift", buffered: true });
```
`sources` lists up to five shifted nodes with before/after rectangles. The shifted node is often a victim; the cause is usually an element above it that changed size.

## 3. DevTools
- Performance panel: Layout shifts track (clusters), each with **culprits** (unsized image, web font swap, injected iframe/ad, late DOM insertion) in recent Chrome.
- Rendering tab > Layout Shift Regions flashes shifted areas while you use the page.

## 4. Field attribution
```js
import { onCLS } from "web-vitals/attribution";
onCLS(({ value, attribution }) => send({ value, target: attribution.largestShiftTarget,
  time: attribution.largestShiftTime, loadState: attribution.loadState }));
```
Group by template and `largestShiftTarget`; `loadState` tells whether it happened during load or later (late-loading ads, infinite scroll, cookie banners, client-side navigations).

## 5. Lab vs field gap
Field CLS covers the whole page lifetime, so shifts after load (late ads, infinite scroll, cookie banners, client-side navigations) count; a load-time lab run can miss them. If field CLS is bad but the lab run is clean, interact with the page and scroll with Layout Shift Regions on.

## Checked
2026-10-31. Confirmed on web.dev (CLS, debug-layout-shifts), MDN LayoutShift and the web-vitals README: session windows (under 1 s gap, 5 s max), 500 ms hadRecentInput, up to five sources, Layout shifts track and culprits insight, Rendering > Layout Shift Regions, largestShiftTarget, largestShiftTime and loadState. Removed: network-throttling advice and the Lighthouse-measures-load-only and bfcache claims.
Method: documentation only; no commands were run.

## Verify
- [ ] Each top shift source from RUM is reproduced locally and fixed (reserved space, font metric overrides, transform animations); p75 CLS < 0.1.
