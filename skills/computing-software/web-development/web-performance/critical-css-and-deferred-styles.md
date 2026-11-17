---
id: computing-software.web-development.web-performance.critical-css-and-deferred-styles
name: critical-css-and-deferred-styles
category: computing-software
field: web-development
product: web-performance
tags: [critical-rendering-path, resource-hints, critical-css, render-blocking-css, inline-css, media-print-swap, css-code-splitting, render-blocking-resources]
level: practitioner
status: docs-checked
description: "Cutting render-blocking CSS: inlining critical above-the-fold styles, loading the rest without blocking, splitting CSS per route, and measuring the gain."
sources:
  - https://web.dev/learn/performance/optimize-resource-loading
  - https://web.dev/articles/extract-critical-css
  - https://github.com/addyosmani/critical
  - https://web.dev/articles/defer-non-critical-css
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Critical CSS and deferring non-critical styles

**Goal:** first paint isn't blocked waiting for a large stylesheet when only a little CSS is needed for the first viewport.

## 1. Is it worth it?
All `<link rel="stylesheet">` in `<head>` block rendering. If total CSS is small and served from the same origin over HTTP/2 with good caching, critical-CSS extraction gains little and adds complexity. Measure first: Lighthouse "Eliminate render-blocking resources", WebPageTest start render.

## 2. Split before you inline
- Route-level CSS splitting.
- Purge unused CSS, with care.
- Move rarely used styles (print, admin widgets) to separate files.

## 3. Inline critical, load the rest async
```html
<style>/* critical: header, hero, layout above the fold (keep above-the-fold content under 14 KB compressed) */</style>
<link rel="preload" href="/css/site.4f1c.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="/css/site.4f1c.css"></noscript>
```
This preload-plus-`onload` pattern is the one web.dev describes for loading non-critical CSS asynchronously; it isn't the standard way of loading CSS, and the `<noscript>` fallback is needed.

Generate critical CSS with the `critical` tool (see its README) or your framework's support.

## 4. Pitfalls
- **FOUC/CLS**: anything below the fold styled only by the async sheet may jump when it loads; anything above the fold missing from critical CSS flashes. Test real templates and viewports.
- Inlined CSS isn't cached separately - it's re-sent with every HTML response. Keep it small.

## Verify
- [ ] Lighthouse no longer lists the stylesheet as render-blocking; FCP/LCP improve in lab and field.
- [ ] No visible style flash or CLS on mobile and desktop viewports.
- [ ] HTML size increase stays within budget.

## Checked

2026-10-28. Confirmed from web.dev (extract critical CSS: keep above-the-fold content under 14 KB compressed; defer non-critical CSS: the preload plus `onload` pattern with a `<noscript>` fallback, noted as not the standard way of loading CSS). Removed (not found): the 15-20 KB threshold, the `media="print"` swap snippet and its CSP note, Vite/Next splitting claim, Tailwind claim, Beasties and Puppeteer details, the `@import` claim.

Method: documentation only; no commands were run.
