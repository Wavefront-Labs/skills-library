---
id: computing-software.web-development.web-performance.long-animation-frames-attribution
name: long-animation-frames-attribution
category: computing-software
field: web-development
product: web-performance
tags: [inp, long-animation-frames, loaf, rum, performance-observer, attribution, inp-attribution]
level: practitioner
status: docs-checked
description: "Using the Long Animation Frames API (LoAF) to attribute slow interactions to specific scripts in the field: observing entries, reading script attribution, and sending it to RUM."
sources:
  - https://developer.chrome.com/docs/web-platform/long-animation-frames
  - https://developer.mozilla.org/en-US/docs/Web/API/PerformanceLongAnimationFrameTiming
  - https://github.com/GoogleChrome/web-vitals#attribution
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Long Animation Frames (LoAF) attribution

LoAF (Chromium 123+) replaces Long Tasks for diagnosing responsiveness: it reports frames whose rendering was delayed more than 50 ms, including **which scripts ran**, their source URLs, function names and durations - in the field, where lab traces can't reproduce real users' slowness.

## 1. Observe
```js
new PerformanceObserver(list => {
  for (const f of list.getEntries()) {
    if (f.duration < 100) continue;
    const scripts = f.scripts.map(s => ({
      src: s.sourceURL, fn: s.sourceFunctionName, invoker: s.invoker, type: s.invokerType,
      dur: Math.round(s.duration), forcedLayout: Math.round(s.forcedStyleAndLayoutDuration),
    }));
    queueBeacon({ start: f.startTime, dur: f.duration, blocking: f.blockingDuration,
                  renderStart: f.renderStart, styleLayoutStart: f.styleAndLayoutStart, scripts });
  }
}).observe({ type: "long-animation-frame", buffered: true });
```
- `invokerType`: `event-listener`, `user-callback` (timers, rAF), `resolve-promise`, `reject-promise`, `classic-script`, `module-script`.
- `invoker` e.g. `IMG#id.onload`, `Window.requestAnimationFrame`, `Response.json.then`.
- The reported source is the script entry point, not necessarily the slow function: if a handler calls a slow library function, the handler is reported.
- `forcedStyleAndLayoutDuration` exposes layout thrashing per script.
- Source entries may be missing for no-cors cross-origin scripts or callbacks not defined in user code; serve your CDN scripts with CORS headers and `crossorigin`.

## 2. With web-vitals
`import { onINP } from "web-vitals/attribution"` - `attribution.longAnimationFrameEntries` and `longestScript` attach the LoAFs overlapping the INP interaction (`longestScript` covers only scripts over 5 ms). Send `longestScript.entry.sourceURL` and `subpart` (`input-delay`, `processing-duration` or `presentation-delay`) to analytics.

## 3. Analyse
Aggregate by script origin/URL and invoker across sessions: you'll typically find a few third-party scripts or one of your bundles' event handlers dominating. Prioritise by total blocking time contributed to INP interactions.

## 4. Caveats
- Shipped in Chromium 123; feature-detect and sample to limit beacon volume.
- Source positions point at minified code - map with source maps offline.
- All handlers of the same promise are mixed together as one script entry.

## Checked
2026-10-31. Confirmed on the Chrome LoAF page, MDN and the web-vitals README: 50 ms threshold, Chromium 123, invokerType values, forcedStyleAndLayoutDuration, entry-point attribution, missing sources for no-cors scripts, longestScript and subpart values. Removed: the v4+ version gate and the nested-promise duration claim.
Method: documentation only; no commands were run.

## Verify
RUM dashboard lists top scripts by LoAF duration during INP interactions; after fixing the top offender, its share and field INP p75 drop.
