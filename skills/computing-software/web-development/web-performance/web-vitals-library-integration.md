---
id: computing-software.web-development.web-performance.web-vitals-library-integration
name: web-vitals-library-integration
category: computing-software
field: web-development
product: web-performance
tags: [web-vitals-library, rum, core-web-vitals, attribution-build, analytics]
level: practitioner
status: verified
description: "Integrating Google's web-vitals library for RUM: onLCP/onINP/onCLS, the attribution build, sending beacons to analytics or your own endpoint, sampling, and aggregating at p75."
sources:
  - https://github.com/GoogleChrome/web-vitals
  - https://web.dev/articles/vitals-measurement-getting-started
  - https://web.dev/articles/debug-performance-in-the-field
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Integrating the web-vitals library

The `web-vitals` package (about 3 KB brotli per its README) measures Core Web Vitals the same way Chrome reports them to CrUX.

## 1. Basic setup
```js
import { onLCP, onINP, onCLS, onFCP, onTTFB } from "web-vitals";

function send(metric) {
  const body = JSON.stringify({
    name: metric.name, value: metric.value, rating: metric.rating,   // "good" | "needs-improvement" | "poor"
    delta: metric.delta, id: metric.id, navigationType: metric.navigationType,
    page: location.pathname,
  });
  (navigator.sendBeacon && navigator.sendBeacon("/rum", body)) || fetch("/rum", { body, method: "POST", keepalive: true });
}
onLCP(send); onINP(send); onCLS(send); onFCP(send); onTTFB(send);
```
- Call each `on*` once per page load; they report when the value is final (often on page hide), and may report again with `delta` for CLS/INP updates if `reportAllChanges` is set.
- Use `metric.id` to de-duplicate and `delta` when summing in tools like GA4.
- `onFID()` was removed in v5.0.0 (May 2025); INP replaces it. Current release checked: 6.2.3.
- `metric.navigationType` is one of `navigate`, `reload`, `back-forward`, `back-forward-cache`, `prerender`, `restore` or `soft-navigation` (from the package's type definitions).

## 2. Attribution build
```js
import { onINP, onLCP, onCLS } from "web-vitals/attribution";
onINP(({ value, attribution }) => send({ name: "INP", value,
  target: attribution.interactionTarget, type: attribution.interactionType,
  inputDelay: attribution.inputDelay, processing: attribution.processingDuration,
  presentation: attribution.presentationDelay, loaf: attribution.longAnimationFrameEntries?.length }));
onLCP(({ value, attribution }) => send({ name: "LCP", value, el: attribution.target,
  ttfb: attribution.timeToFirstByte, loadDelay: attribution.resourceLoadDelay,
  loadTime: attribution.resourceLoadDuration, renderDelay: attribution.elementRenderDelay }));
onCLS(({ value, attribution }) => send({ name: "CLS", value, el: attribution.largestShiftTarget }));
```
Slightly larger (about 1.5 KB more, brotli, per the README) but tells you *why*: which element, which interaction, which LCP subpart.

## 3. Destinations
- GA4: `gtag("event", name, { value: delta, metric_id: id, metric_value: value, metric_rating: rating })`, then BigQuery export for p75.
- Own endpoint -> ClickHouse/BigQuery; or vendors (SpeedCurve, DebugBear, Sentry, Datadog RUM) that accept web-vitals data.
- Sample high-traffic sites (e.g. 10% of sessions) but keep it consistent per session.

## 4. Analysis
Aggregate at the **75th percentile** per page template and device class (mobile/desktop), over 28 days to match CrUX. Segment by `navigationType` (back-forward cache restores, prerender) and by country/connection.

## 5. Gotchas
- Load the library early (inline or high in the bundle) or `onLCP`/`onCLS` miss early entries; it buffers via `buffered: true` PerformanceObservers, so async loading is OK as long as it runs before page hide.
- Browser support per the web-vitals README: `onCLS()` is Chromium only; `onFCP()`, `onINP()`, `onLCP()` and `onTTFB()` run in Chromium, Firefox and Safari. Expect no CLS rows from Firefox or Safari, and check the `rating` distribution by browser.

## Verify
- [ ] Beacons arrive on page hide for all metrics; p75 per template in your dashboard roughly matches CrUX; attribution fields populated for poor INP/LCP.
