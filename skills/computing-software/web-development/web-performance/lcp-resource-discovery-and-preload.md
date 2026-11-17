---
id: computing-software.web-development.web-performance.lcp-resource-discovery-and-preload
name: lcp-resource-discovery-and-preload
category: computing-software
field: web-development
product: web-performance
tags: [lcp, lcp-preload, lcp-discovery, fetchpriority, preload, core-web-vitals]
level: practitioner
status: docs-checked
description: "Making the LCP image or font discoverable early: avoiding lazy-loading and JS/CSS-only references, preload with imagesrcset, fetchpriority=high, and measuring load delay."
sources:
  - https://web.dev/articles/optimize-lcp
  - https://web.dev/articles/fetch-priority
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/rel/preload
  - https://web.dev/articles/lcp-lazy-loading
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Making the LCP resource discoverable

"Resource load delay" (time from TTFB until the browser starts fetching the LCP resource) is often the biggest LCP sub-part. Goal: the preload scanner finds the LCP image in the initial HTML and requests it at high priority.

## 1. Anti-patterns that hide the LCP resource
- `loading="lazy"` on the hero image - it waits for layout.
- Image set via CSS `background-image` in an external stylesheet - discovered only after CSS downloads and applies.
- Image inserted by JavaScript (client-rendered hero, carousel library, `data-src` lazy loaders).

## 2. Fixes
```html
<!-- Best: plain img in server HTML -->
<img src="/hero-1200.avif" srcset="/hero-800.avif 800w, /hero-1200.avif 1200w, /hero-2000.avif 2000w"
     sizes="100vw" width="1200" height="600" alt="…" fetchpriority="high" decoding="async">
```
- `fetchpriority="high"` hints high relative priority for the LCP image (web.dev Fetch Priority); use it on one or two images only.
- If it must be a CSS background or JS-inserted, preload it:
```html
<link rel="preload" as="image" href="/hero-1200.avif" imagesrcset="/hero-800.avif 800w, /hero-1200.avif 1200w" imagesizes="100vw" fetchpriority="high">
```
  Preloads must match what's actually used (same URL/srcset) or you double-download. Responsive `<picture>` with art direction: preload with `media` attributes per source.
- Serve the image from the same origin or `preconnect` to the image CDN (`<link rel="preconnect" href="https://img.example.com" crossorigin>` only if fetched with CORS).
- Text LCP with web fonts: preload the one critical WOFF2 (`<link rel="preload" as="font" type="font/woff2" crossorigin href=...>`), use `font-display: swap|optional`.

## 3. Measure
- In the DevTools Network panel the priority column should show "High" for the LCP image, and its request should start near the top of the waterfall.

## Verify
Resource load delay is a small share of LCP (web.dev's guideline is under 10%); the LCP image request starts within the first few requests in WebPageTest.

## Checked

2026-10-28. Confirmed from web.dev Optimize LCP (resource load delay guideline under 10% of LCP; images in CSS `background-image` and lazy-loaders using `data-src` are not discoverable by the preload scanner), web.dev Fetch Priority and the MDN `rel=preload` page (`imagesrcset`, `media`). Removed (not found): the HTTP Archive 10% figure, the consent-banner example, framework image components, the Lighthouse audit name and the web-vitals attribution call.

Method: documentation only; no commands were run.
