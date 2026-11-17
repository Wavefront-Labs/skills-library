---
id: computing-software.web-development.web-performance.cls-reserved-space-for-dynamic-content
name: cls-reserved-space-for-dynamic-content
category: computing-software
field: web-development
product: web-performance
tags: [cls, reserved-space, ads, embeds, cookie-banners, layout-shift, ad-slot-sizing, cookie-banner-cls]
level: practitioner
status: docs-checked
description: "Reserving space for ads, embeds, banners and late-loading content to prevent CLS: min-height slots, overlays for notices, skeletons, and inserting content without pushing."
sources:
  - https://web.dev/articles/optimize-cls
  - https://developers.google.com/publisher-tag/guides/minimize-layout-shift
  - https://web.dev/articles/debug-layout-shifts
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Reserved space for dynamic content

## 1. Ads
```css
.ad-slot-mpu { min-height: 250px; min-width: 300px; }
.ad-slot-leaderboard { min-height: 90px; }
@media (width < 728px) { .ad-slot-leaderboard { min-height: 50px; } }
```
- Use `min-height`/`min-width` so the slot reserves space but can still grow. With variable sizes, start at the smallest size that will be used and accept some shift for larger ads.
- Collapsing empty slots (Google Publisher Tag `collapseDiv`) can itself cause shifts. Using historical fill data, start slots that are likely to fill expanded and slots unlikely to fill collapsed.
- Slots near the top of the initial viewport displace the most content; take special care with them.

## 2. Banners and notices
Cookie consent, promo bars and similar notices: reserve space for them in advance (placeholder or skeleton), or take them out of the document flow by overlaying the content. Injecting a bar after load pushes the page down.

## 3. Late content
- Skeletons sized like the final content (same heights) for async sections.
- If you cannot reserve space, place injected content later on the page; content nearer the top of the viewport shifts more.
- Let the user start the load (a "Load more" or "Refresh" button); layout shifts within 500 ms of user input are not counted towards CLS. Prefetch so content appears immediately.
- For live feeds, load content offscreen and overlay a notice (for example a "Scroll to top" button) instead of prepending.
- Responsive embeds and ads: `min-height` or `aspect-ratio` on the wrapper. Images and video need `width` and `height` attributes (or `aspect-ratio`).

## 4. Animations and transitions
Animate with `transform` (translate, scale, rotate, skew), which does not trigger re-layout, instead of properties that do.

## 5. Find shifts
- DevTools: the Layout shift culprits insight in the Performance panel's Insights lists possible causes. Lighthouse often lists the elements that moved, not the one that caused the shift.
- Field data: the web-vitals library has attribution functions for CLS.
- `PerformanceObserver` on `layout-shift` entries; each entry's `sources` lists up to five moved DOM elements.

## Verify
Field CLS at the 75th percentile is 0.1 or less (poor is above 0.25); no shifts are reported while ads, banners and async sections load on a throttled connection.

## Checked
2026-11-01. Confirmed against web.dev Optimize CLS and Debug layout shifts, and the Google Publisher Tag minimize-layout-shift guide (min-height/min-width, collapseDiv, 500 ms input exclusion, transform, 0.1 and 0.25 thresholds, sources limit). Removed the pixel-size examples as guidance, `position: fixed`, accordion exclusion and `largestShiftTarget` names (not in the fetched pages).
Method: documentation only; no commands were run.
