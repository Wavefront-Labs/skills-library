---
id: computing-software.software-engineering.javascript.js-performance-api-and-measurement
name: js-performance-api-and-measurement
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-performance-api, performance-mark, performance-observer, web-vitals, long-tasks]
level: advanced
status: draft
description: "Measure real performance with performance.now, marks and measures, PerformanceObserver and Core Web Vitals."
sources: ["https://tc39.es/ecma262/", "https://developer.mozilla.org/en-US/docs/Web/JavaScript"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Performance API

- `performance.now()` is a monotonic high-resolution clock (ms since time origin); do not use `Date.now()` for durations.
- User timing: `performance.mark("a")`, `performance.measure("a-to-b", "a", "b")`; they show in DevTools Performance panel timings.
- `new PerformanceObserver(list => ..., ).observe({ type: "largest-contentful-paint", buffered: true })` for LCP, `layout-shift` (CLS), `event` (INP), `longtask`, `resource`, `navigation`.
- Core Web Vitals: LCP (loading), INP (responsiveness, replaced FID in March 2024), CLS (visual stability); the `web-vitals` library wraps them for field (RUM) reporting. Lab tools (Lighthouse) and field data (CrUX) differ; trust field data.
- Micro-benchmarks: warm up, run many iterations, defeat dead-code elimination, compare medians; engines JIT differently across runs.
- Report with `navigator.sendBeacon` so data survives unload.
