---
id: computing-software.web-development.web-performance.non-composited-animations-and-layout-shifts
name: non-composited-animations-and-layout-shifts
category: computing-software
field: web-development
product: web-performance
tags: [layout-shift-animations, cls, non-composited-animations, compositor-animations, performance]
level: practitioner
status: docs-checked
description: "Stopping animations from causing CLS and jank: which properties shift layout, replacing top/left/height animations with transforms, and finding offenders."
sources:
  - https://web.dev/articles/optimize-cls#animations
  - https://developer.chrome.com/docs/lighthouse/performance/non-composited-animations
  - https://web.dev/articles/animations-guide
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Non-composited animations causing layout shifts

## 1. What counts
CLS records shifts when a visible element's start position changes between frames without recent user input. Animating layout properties moves elements every frame:
- Properties such as `width`, `height`, `left` and `top` require layout (web.dev), so animating them moves elements every frame, and everything after them.
- `transform` and `opacity` are the properties web.dev recommends for animation because they avoid layout and paint.

Common offenders: banners sliding down by animating `height` from 0, carousels moving with `left`, accordion auto-height animations above content, "toast" pushes that change margin, skeleton-to-content height jumps.

## 2. Fixes
```css
/* Bad: pushes content down every frame */
.banner { height: 0; transition: height .3s; } .banner.open { height: 64px; }
/* Good: overlay that doesn't affect layout, moved with transform */
.banner { position: fixed; inset-inline: 0; top: 0; translate: 0 -100%; transition: translate .3s; }
.banner.open { translate: 0 0; }
```
- Carousels: `transform: translateX()` on the track, or native scroll-snap.
- Infinite marquee/ticker: transform only.

## 3. Find them
- Lighthouse and DevTools can flag non-composited animations (see the Lighthouse non-composited animations page).
- A `PerformanceObserver` for `layout-shift` entries in RUM.

## 4. Jank side effect
Even when not counted (out of viewport, after input), layout-property animations re-run layout every frame: watch for long "Layout" bars and dropped frames on low-end Android.

## Verify
- [ ] No animation of layout properties outside user-triggered disclosures; Lighthouse non-composited audit clean.

## Checked

2026-10-28. Confirmed from web.dev (properties such as `width`, `height`, `left`, `top` require layout; animate `transform` and `opacity`; reserving space and `font-display`/`size-adjust` guidance on the CLS page) and the Chrome pages' mention of `layout-shift` entries. Removed (not found): the 500 ms input grace period for ordinary CLS, the full property list, `interpolate-size`, Lighthouse reason strings and the Layout Shift Regions and Layout Shifts track claims.

Method: documentation only; no commands were run.
