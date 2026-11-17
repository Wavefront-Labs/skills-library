---
id: computing-software.web-development.frontend-development.easing-functions-and-linear
name: easing-functions-and-linear
category: computing-software
field: web-development
product: frontend-development
tags: [easing-functions, linear-easing, cubic-bezier, steps-easing, motion-design, css-animation]
level: practitioner
status: docs-checked
description: "Choosing easing for UI motion: ease-out vs ease-in, cubic-bezier overshoot, steps() for sprites, the linear() function for springs and bounces, and sensible durations."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/easing-function
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/easing-function/linear
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/easing-function/steps
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/easing-function/cubic-bezier
  - https://github.com/mdn/browser-compat-data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Easing functions and linear()

## 1. Rules of thumb (design guidance, not part of any specification)
| Motion | Easing |
|---|---|
| Element entering / expanding | ease-out (fast start, gentle stop) |
| Element leaving | ease-in |
| Moving on screen | ease-in-out |
| Spinners, progress, marquee | linear |
Default `ease` is a reasonable generic choice; `linear` for positional UI motion looks mechanical.

## 2. cubic-bezier
```css
:root {
  --ease-out: cubic-bezier(0.2, 0, 0, 1);
  --ease-in: cubic-bezier(0.3, 0, 1, 1);
  --ease-overshoot: cubic-bezier(0.34, 1.56, 0.64, 1);   /* y > 1 overshoots then settles */
}
.panel { transition: transform 220ms var(--ease-out); }
```
x values must be within 0-1; y may exceed it for anticipation/overshoot. Define motion tokens once.

## 3. steps()
```css
.sprite { animation: walk 0.8s steps(8, end) infinite; }   /* 8 frames of a sprite sheet */
.typing { animation: type 2s steps(20, end); }
```
`jump-start`, `jump-end` (= `end`), `jump-none`, `jump-both` control where jumps occur.

## 4. linear() for springs and bounces (Baseline 2023)
```css
.toast {
  transition: transform 600ms linear(0, 0.36 9%, 0.86 20%, 1.06 30%, 1.07 36%, 1.01 50%, 0.99 62%, 1);
}
```
A piecewise-linear curve through many points approximates spring physics without JavaScript. Generate points with a linear() generator tool from a spring definition; keep a cubic-bezier fallback declared first for older browsers.

## 5. Same values everywhere
Web Animations API and JS libraries accept the same strings (`easing: "cubic-bezier(...)"`, `"linear(...)"`), so share tokens between CSS and JS.

## Gotchas
- Easing applies per keyframe segment in `@keyframes` (set `animation-timing-function` inside keyframes to vary it).
- Respect `prefers-reduced-motion`: shorten or remove movement, keep opacity fades.

## Verify
- [ ] Motion tokens defined once; entering/leaving transitions use ease-out/ease-in respectively.

## Checked

Checked 2026-10-26 against current documentation. MDN easing-function pages (x coordinates of `cubic-bezier()` must be in [0, 1], `steps()` jump keywords, `jump-none` needs more than one step, `linear()`) and browser-compat-data for `linear()` (Chrome 113, Firefox 112, Safari 17.2; Baseline 2023). Fixed: sprite example used `jump-none`, which holds both end frames; now `steps(8, end)`. Removed the duration ranges and Material token source, which are not specified anywhere checked.

Method: documentation only; no commands were run.
