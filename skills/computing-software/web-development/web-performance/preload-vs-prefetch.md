---
id: computing-software.web-development.web-performance.preload-vs-prefetch
name: preload-vs-prefetch
category: computing-software
field: web-development
product: web-performance
tags: [rel-preload, rel-prefetch, resource-hints, preload-pitfalls, imagesrcset, performance]
level: practitioner
status: verified
description: "Choosing preload, prefetch, preconnect and modulepreload: correct as/type/crossorigin attributes, responsive image preloads, unused-preload warnings and over-preloading costs."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/rel/preload
  - https://web.dev/articles/preload-critical-assets
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/rel/prefetch
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# preload vs prefetch

| Hint | For | Priority |
|---|---|---|
| `preload` | resource needed by **this** page, discovered late | high (by type) |
| `modulepreload` | JS modules for this page | high |
| `prefetch` | resource for a **likely next** navigation | lowest, idle |
| `preconnect` | early DNS+TCP+TLS to an origin you will use soon | n/a |
| `dns-prefetch` | DNS only (cheap fallback) | n/a |
| speculation rules | prefetch/prerender whole next pages | see speculation rules |

## 1. Preload correctly
```html
<link rel="preload" href="/fonts/inter-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/css/critical-bg.avif" as="image" type="image/avif">
<link rel="preload" as="image" href="/hero-800.avif"
      imagesrcset="/hero-400.avif 400w, /hero-800.avif 800w, /hero-1600.avif 1600w" imagesizes="100vw">
```
- `as` is required and must match the eventual request; wrong or missing `as` = double download (run in Chromium: `as=script` for an image requested `/j.png` twice, once as `script` and once as `image`).
- Fonts always need `crossorigin` (fonts are fetched in CORS mode even same-origin; run: a same-origin font preload without it was requested twice, with it once).
- `type` lets browsers skip formats they cannot use.
- Responsive images: `imagesrcset`/`imagesizes` must mirror the `<img>` so the same candidate is chosen.
- For an `<img>` already in the HTML, `fetchpriority="high"` is usually better than preloading it.

## 2. Pitfalls
- DevTools warns about preloads that are never used (it did not surface in a headless Playwright run, so check in a real DevTools session): remove the preload or fix the `as`/`crossorigin`/URL mismatch.
- Every preload competes with render-critical CSS and the LCP image. Typical budget: the LCP image, 1-2 critical fonts, a late-discovered critical script/CSS.
- Preloading CSS loads it but does not apply it; `rel=stylesheet` is still needed.
- Preload via HTTP `Link` header works too (and enables 103 Early Hints).

## 3. Prefetch
```html
<link rel="prefetch" href="/checkout/app-chunk.js">
```
Stored in the HTTP cache on disk (MDN), so it is useful even for resources the current page does not use. Use for the next step of a flow; skip on `navigator.connection.saveData`. For full pages prefer speculation rules.

## Verify
- [ ] Network panel: preloaded resources start early, are used (no warnings), and are not fetched twice.
