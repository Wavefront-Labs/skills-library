---
id: computing-software.web-development.web-performance.render-blocking-resources
name: render-blocking-resources
category: computing-software
field: web-development
product: web-performance
tags: [render-blocking, render-blocking-resources, blocking-render, critical-rendering-path, performance]
level: practitioner
status: docs-checked
description: "Eliminating render-blocking resources: which CSS and scripts block first paint, async/defer/module, media-scoped CSS, the blocking=render attribute, and measuring render delay."
sources:
  - https://web.dev/articles/critical-rendering-path/render-blocking-css
  - https://developer.chrome.com/docs/lighthouse/performance/render-blocking-resources
  - https://html.spec.whatwg.org/multipage/urls-and-fetching.html#blocking-attributes
  - https://developer.chrome.com/docs/performance/insights/render-blocking
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Render-blocking resources and blocking=render

## 1. What blocks rendering
| Resource | Blocks first paint? |
|---|---|
| `<link rel="stylesheet">` in head (matching media) | yes |
| `<link rel="stylesheet" media="print">` | no (downloaded at low priority) |
| `<script src>` in head without async/defer/module | yes, and blocks parsing |

## 2. Fixes
```html
<head>
  <style>/* critical above-the-fold CSS */</style>
  <link rel="stylesheet" href="/app.css">                    <!-- or load async if critical CSS is inlined -->
  <link rel="stylesheet" href="/print.css" media="print">
  <script src="/app.js" defer></script>
  <script src="https://analytics.example/a.js" async></script>
</head>
```
- Move every head script to `defer`/`module` unless it must run before paint (theme detection to avoid a dark-mode flash is a legit small inline exception).

## 3. blocking="render"
```html
<script type="module" src="/theme.js" blocking="render"></script>
```
Per the HTML Standard, the `blocking` attribute takes the token `render`, which marks the element as potentially render-blocking. Use it sparingly and only for tiny critical resources.

## 4. Measuring
- Lighthouse / DevTools Performance insight "Render-blocking requests" lists the requests that blocked the first paint.
- Compare FCP before and after.

## Verify
- [ ] Only critical CSS and intentional `blocking=render` items block paint; no parser-blocking scripts in head; FCP improved on throttled mobile.

## Checked

2026-10-28. Confirmed from web.dev (render-blocking CSS; parser-blocking `<script>` without `async` or `defer`; non-matching media CSS loads at lowest priority), the Chrome Render-blocking requests insight and the HTML Standard blocking attributes section (`blocking` token `render`). Removed (not found): the defer/module/async/@import/web-font table rows, the 10-15 KB figure, Chromium 105+ and `rel=expect` claims, the Render blocking column and WebPageTest indicator claims.

Method: documentation only; no commands were run.
