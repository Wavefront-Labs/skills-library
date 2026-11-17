---
id: computing-software.web-development.frontend-development.css-gradients
name: css-gradients
category: computing-software
field: web-development
product: frontend-development
tags: [css-gradients, conic-gradient, linear-gradient, radial-gradient, gradient-interpolation, css-color]
level: practitioner
status: docs-checked
description: "Linear, radial and conic gradients: stops, hints and hard stops, interpolating in oklch to avoid grey midpoints, repeating patterns, gradient text and animating gradients."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/gradient
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Images/Using_gradients
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/color-interpolation-method
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/gradient/conic-gradient
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CSS gradients

## 1. The three types
```css
.a { background: linear-gradient(135deg, #4f46e5, #ec4899); }
.b { background: radial-gradient(circle at 30% 20%, #fff 0, #c7d2fe 40%, transparent 70%); }
.c { background: conic-gradient(from -90deg, #22c55e 0 72%, #e5e7eb 72% 100%); border-radius: 50%; }  /* pie/progress ring */
```
Gradients are `<image>` values: they go in `background-image` (or `mask-image`, `border-image`), not `background-color`.

## 2. Stops
- Two positions on one stop create a hard edge: `linear-gradient(90deg, red 0 50%, blue 50% 100%)`.
- A colour hint (bare percentage between stops) moves the midpoint: `linear-gradient(red, 20%, blue)`.
- Stripes: `repeating-linear-gradient(45deg, #000 0 10px, #ff0 10px 20px)`.

## 3. Interpolation colour space
MDN documents Oklab as the default interpolation space for `<color>` values; state the space explicitly with `in <space>` when the midpoint colour matters:
```css
.d { background: linear-gradient(in oklch, #4f46e5, #f59e0b); }
.e { background: linear-gradient(in oklch longer hue, red, red); }    /* full rainbow */
```
Browsers that do not understand `in <space>` drop the whole declaration, so put a plain gradient declaration first.

## 4. Gradient text
```css
.title { background: linear-gradient(90deg, #4f46e5, #ec4899); background-clip: text; color: transparent; }
```
Check contrast against the background at both ends, and test in forced-colors mode with an explicit fallback: `@media (forced-colors: active) { .title { color: CanvasText; } }`.

## 5. Animating
Animate registered custom properties used inside the gradient rather than `background-image` itself:
```css
@property --angle { syntax: "<angle>"; inherits: false; initial-value: 0deg; }
.spin { background: conic-gradient(from var(--angle), #4f46e5, #ec4899, #4f46e5); animation: rot 4s linear infinite; }
@keyframes rot { to { --angle: 360deg; } }
```
Or animate `background-position` on an oversized gradient.

## Verify
- [ ] Gradients readable in dark mode and forced-colors; text over gradients meets contrast at the lightest point.

## Checked

Checked 2026-10-26 against current documentation. MDN gradient guide and `<color-interpolation-method>` page: hard stops and two-position stops, colour hints, `in oklch longer hue` syntax, repeating gradients, default interpolation space (documented as Oklab). Removed unconfirmed claims about premultiplied transparent, banding, and forced-colors background handling.

Method: documentation only; no commands were run.
