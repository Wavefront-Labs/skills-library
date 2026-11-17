---
id: computing-software.web-development.tailwind-css.compositor-only-animations
name: compositor-only-animations
category: computing-software
field: web-development
product: tailwind-css
tags: [css-animations, css-transitions, compositor-animations, will-change, transform-opacity, layer-promotion, jank, gpu-acceleration]
level: practitioner
status: docs-checked
description: "Keeping animations on the compositor thread with transform/opacity, using will-change sparingly, FLIP technique for layout changes and diagnosing jank."
sources:
  - https://web.dev/articles/animations-guide
  - https://web.dev/articles/stick-to-compositor-only-properties-and-manage-layer-count
  - https://developer.mozilla.org/en-US/docs/Web/CSS/will-change
  - https://aerotwist.com/blog/flip-your-animations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compositor-only animations

**Goal:** smooth animations that stay smooth even when the main thread is busy.

## 1. The rule
Animate only **`transform`** (translate/scale/rotate) and **`opacity`**. These can run on the compositor without layout or paint. Avoid animating layout-affecting properties such as `top`, `left`, `width` and `height`.

| Want | Do instead |
|---|---|
| Move element | `transform: translate()` |
| Grow a panel | `transform: scaleY()` on a wrapper, or FLIP |
| Animated shadow | Fade `opacity` of a pseudo-element that has the final shadow |

## 2. will-change
`will-change: transform` promotes an element to its own layer ahead of time, avoiding a first-frame hitch. But do not apply it to too many elements and use it sparingly: the browser already optimizes, and too many hints can slow the page (MDN). Apply it shortly before the change and remove it after.

## 3. FLIP for layout transitions
First (measure), Last (apply new layout, measure), Invert (transform back to First), Play (animate transform to none):
```js
const first = el.getBoundingClientRect();
container.classList.toggle('expanded');
const last = el.getBoundingClientRect();
el.animate([{ transform: `translate(${first.left-last.left}px, ${first.top-last.top}px) scale(${first.width/last.width}, ${first.height/last.height})` }, { transform: 'none' }],
  { duration: 250, easing: 'ease-out' });
```

## 4. Diagnose
Use your browser's DevTools rendering and performance panels to see repaints, layout work per frame and layer count.

## Verify
- [ ] DevTools shows no repaint or layout during the animation.
- [ ] Animation stays smooth with CPU throttling enabled.
- [ ] Layer count reasonable and `will-change` removed after use.

## Checked
2026-10-28 Confirmed on web.dev (compositor-only properties and layer count), MDN will-change (do not apply to too many elements; use sparingly; remove after) and the Aerotwist FLIP article (First, Last, Invert, Play). Removed: fps figures, filter, paint/layout lists beyond top/left/width/height, interpolate-size, GPU-memory/crash claim, View Transitions claim, DevTools panel colours, CPU throttling factor.
Method: documentation only; no commands were run.
