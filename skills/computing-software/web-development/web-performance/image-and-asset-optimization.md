---
id: computing-software.web-development.web-performance.image-and-asset-optimization
name: image-and-asset-optimization
category: computing-software
field: web-development
product: web-performance
tags: [images, avif, webp, srcset, lazy-loading, lcp, fonts, font-display, performance, cls, web-development]
level: advanced
status: docs-checked
description: "Web image/font optimization: AVIF/WebP with fallback, srcset/sizes for responsive images, lazy-loading without hurting LCP, and font-display strategy."
sources:
  - https://web.dev/articles/choose-the-right-image-format
  - https://web.dev/articles/optimize-cls
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Image and asset optimization — bytes you don't need to send

**Goal:** ship the smallest correct asset for each viewport/device without
hurting LCP (the thing users actually feel) in the process of trying to help it.

## 1. Format choice
- **AVIF** and **WebP** are modern raster formats alongside PNG and JPEG (web.dev, choose the right image format); check your target browser matrix and encoders before standardising on one.
- **`<picture>` with multiple sources** gets the browser to pick the best it
  supports, with a universal JPEG/PNG fallback:
```html
<picture>
  <source srcset="hero.avif" type="image/avif">
  <source srcset="hero.webp" type="image/webp">
  <img src="hero.jpg" alt="…" width="1200" height="600">
</picture>
```
- Prefer **SVG** for vector artwork; raster formats suit photographs (web.dev, choose the right image format).
- Always set explicit `width`/`height` (or `aspect-ratio` in CSS) — the browser
  reserves space before the image loads, which is what actually prevents layout
  shift (CLS), not the format choice.

## 2. Responsive images — `srcset`/`sizes`, not one giant file for everyone
```html
<img srcset="photo-400.jpg 400w, photo-800.jpg 800w, photo-1600.jpg 1600w"
     sizes="(max-width: 600px) 100vw, 50vw"
     src="photo-800.jpg" alt="…">
```
`sizes` tells the browser the image's rendered width at each breakpoint *before*
it knows the final layout — get this wrong and the browser picks a bigger (or
smaller, causing blur) candidate than it needs. `srcset` without `sizes` only
helps with device pixel ratio, not viewport width.

## 3. Lazy loading — only below the fold, never on the LCP image
```html
<img src="below-fold.jpg" loading="lazy" alt="…">
<img src="hero.jpg" fetchpriority="high" alt="…">  <!-- LCP candidate: eager, high priority -->
```
`loading="lazy"` on the hero/LCP image delays the exact image Core Web Vitals is measuring. Use `fetchpriority="high"` on the identified LCP image and
leave images that are off-screen as `lazy`.

## 4. Font loading — avoid invisible text and layout shift
```css
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter.woff2') format('woff2');
  font-display: swap;   /* show fallback immediately, swap when custom font loads */
}
```
- `font-display: swap` avoids FOIT (invisible text) but can cause a visible
  reflow when the swap happens — mitigate with `size-adjust`/matched fallback
  metrics, or `font-display: optional` if the swap-triggered shift is worse than
  using the fallback font permanently for slow connections.
- `<link rel="preload" as="font" type="font/woff2" crossorigin>` for the
  above-the-fold font so it starts fetching immediately instead of waiting for
  the CSS that references it to parse.

## 5. General asset hygiene
- Serve images from a CDN or image service that resizes on the fly rather than hand-generating every size.
- Compress images with a real tool at build or upload time, not default design-tool exports.
- Run SVGs from design tools through an optimizer to strip unnecessary metadata.

## Verify
- [ ] The LCP image is `fetchpriority="high"` and never `loading="lazy"`.
- [ ] Every image has explicit dimensions or `aspect-ratio` to prevent layout shift.
- [ ] `srcset`/`sizes` (or an image CDN) serves an appropriately sized file per viewport, not one large file for all.
- [ ] Above-the-fold custom fonts are preloaded; `font-display` is set deliberately.
- [ ] SVGs are run through an optimizer before shipping.

## Checked

2026-10-28. Confirmed from web.dev (choose the right image format: PNG, JPEG, WebP, AVIF as raster formats; optimize CLS: `width`/`height` or `aspect-ratio`, FOUT versus FOIT, `font-display: optional` avoids a re-layout, `size-adjust`) and the MDN `rel=preload` page (`imagesrcset`, `type`, `media`). Removed (not found): the 25-35% WebP figure, AVIF superlatives, the self-hosting claim, tool names, and the dead web.dev font-display link (replaced with the CLS page).

Method: documentation only; no commands were run.
