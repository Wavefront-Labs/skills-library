---
id: computing-software.software-engineering.javascript.js-web-vitals-measurement
name: js-web-vitals-measurement
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, web-vitals, js-performance]
level: practitioner
status: docs-checked
description: "Core Web Vitals thresholds at the 75th percentile, measuring LCP, INP and CLS in the field with the web-vitals library, and why lab tools cannot measure INP."
sources: ["https://web.dev/articles/vitals"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Core Web Vitals measurement

- Core Web Vitals (stable): Largest Contentful Paint (LCP) within 2.5 s of page load start; Interaction to Next Paint (INP) of 200 ms or less; Cumulative Layout Shift (CLS) of 0.1 or less. Assess the 75th percentile of page loads, segmented across mobile and desktop; a page passes if all three meet the targets at that percentile.
- Easiest field measurement: the `web-vitals` library. The page's example is `import {onCLS, onINP, onLCP} from 'web-vitals';` then calling each with a callback that JSON-stringifies the metric and sends it with `navigator.sendBeacon()`, falling back to `fetch()` with `keepalive: true`.
- Metrics measured in JavaScript with public APIs may differ from those CrUX reports. The page links separate guides for measuring LCP, INP and CLS with the underlying web APIs.
- CrUX (also behind DevTools, PageSpeed Insights and Search Console) gives quick field data but not per-pageview telemetry, so the page strongly recommends your own real-user monitoring.
- Lab tools such as Lighthouse load pages in a simulated environment with no user input, so they cannot measure INP; Total Blocking Time (TBT) is the lab proxy. Lab testing does not replace field measurement because device, network and interaction vary.
- Per-metric optimisation guides exist for LCP, INP and CLS; the page does not give the fixes itself.

Self-check: the aggregated 75th-percentile LCP, INP and CLS from your analytics endpoint are each compared with the 2.5 s, 200 ms and 0.1 targets.

## Checked

Confirmed on the web.dev "Web Vitals" article (updated October 2024): thresholds, 75th-percentile rule, web-vitals usage and example, CrUX limits, lab versus field and INP. Removed: the attribution build, the raw `PerformanceObserver` example, the "compare with the CrUX report" self-check, and the specific fixes (`fetchpriority`, sized media, trimming long tasks), which this page defers to other guides.

Method: docs-only read of cited pages, 2026-11-08
