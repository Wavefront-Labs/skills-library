---
id: computing-software.web-development.frontend-development.animating-height-auto
name: animating-height-auto
category: computing-software
field: web-development
product: frontend-development
tags: [interpolate-size, animate-height-auto, calc-size, transition-behavior, accordion-animation, css-animation]
level: practitioner
status: docs-checked
description: "Animating to and from height auto: interpolate-size allow-keywords, calc-size(), and display none with transition-behavior allow-discrete."
sources:
  - https://developer.chrome.com/docs/css-ui/animate-to-height-auto
  - https://developer.mozilla.org/en-US/docs/Web/CSS/interpolate-size
  - https://developer.mozilla.org/en-US/docs/Web/CSS/transition-behavior
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Animating height auto

## 1. Modern: interpolate-size (Chromium 129+)
```css
:root { interpolate-size: allow-keywords; }        /* opt in once; inherited */
.panel { height: 0; overflow: clip; transition: height 250ms ease-out; }
.panel.open { height: auto; }
```
Per-element alternative: `height: calc-size(auto, size)`; use it when the animation also needs calculations (`interpolate-size` is preferred otherwise). One end of the animation must be a length or percentage; intrinsic-to-intrinsic is not animated. MDN marks `interpolate-size` as not Baseline, so keep a fallback.

## 3. Animating to/from display: none
```css
.toast { transition: opacity 200ms, display 200ms allow-discrete; }   /* transition-behavior: allow-discrete */
.toast[hidden] { opacity: 0; display: none; }
```
`transition-behavior: allow-discrete` lets discrete properties such as `display` and `content-visibility` flip at the end of the transition instead of immediately.

## Gotchas
- Honour `prefers-reduced-motion: reduce` by removing the transition.

## Checked
2026-10-31. Confirmed on the Chrome animate-to-height-auto article and MDN `interpolate-size` and `transition-behavior`: Chrome 129, `allow-keywords`, inheritance, `calc-size(auto, size)`, one end must be a length-percentage, `allow-discrete` for display and content-visibility. Removed: the details `::details-content` section, the max-height hack claims, the layout-cost claim and the all-browsers claim for the grid fallback (not on those pages).
Method: documentation only; no commands were run.

## Verify
- [ ] Accordion opens/closes smoothly in Chromium and degrades to instant toggle (or grid fallback) in others; content never clipped.
