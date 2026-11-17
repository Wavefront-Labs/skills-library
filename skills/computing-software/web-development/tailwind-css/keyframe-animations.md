---
id: computing-software.web-development.tailwind-css.keyframe-animations
name: keyframe-animations
category: computing-software
field: web-development
product: tailwind-css
tags: [css-animations, css-transitions, keyframes, animation-properties, animation-fill-mode, animationend, steps-timing]
level: practitioner
status: docs-checked
description: "Writing @keyframes animations: animation shorthand, fill-mode, iteration and direction, timing functions incl. steps() and linear(), and JS control via events."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@keyframes
  - https://developer.mozilla.org/en-US/docs/Web/CSS/animation
  - https://developer.mozilla.org/en-US/docs/Web/CSS/easing-function
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# @keyframes animations

**Goal:** declarative animations that start, end and loop exactly as designed.

## 1. Define and apply
```css
@keyframes slide-in {
  from { transform: translateY(1rem); opacity: 0; }
  to   { transform: none; opacity: 1; }
}
.toast { animation: slide-in 200ms cubic-bezier(.2,.8,.2,1) both; }
```
Shorthand order is flexible but the first time value is duration, the second is delay: `animation: name duration easing delay iteration-count direction fill-mode play-state`.

## 2. Properties that bite
- **`animation-fill-mode`**: without `forwards`/`both`, the element snaps back to its pre-animation style at the end; `backwards`/`both` applies the first keyframe during the delay (prevents a flash before a delayed entrance).
- **`animation-iteration-count: infinite`** + **`animation-direction: alternate`** for pulses.
- To restart an animation, change `animation-name` or use the Web Animations API.
- Multiple animations: comma-separated lists; later ones override the same property.

## 3. Timing functions
- `ease-out`-like curves for entrances, `ease-in` for exits, `linear` for spinners.
- `steps(8, end)` for sprite sheets / typewriter effects.
- `linear(0, 0.25 25%, 1)` (multi-point linear) approximates springs/bounces in pure CSS.

## 4. JS hooks
```js
el.addEventListener('animationend', (e) => { if (e.animationName === 'slide-out') el.remove(); }, { once: true });
```
Do not rely only on `animationend` when the element can be removed, hidden or have animations disabled mid-animation; keep a timeout fallback.

## 5. Performance
Prefer animating `transform` and `opacity`; check the Performance panel for layout and paint work (see compositor animations skill).

## Verify
- [ ] Animation ends in the intended state (fill-mode) and doesn't flash at start.
- [ ] Removal-after-exit works with reduced motion on.
- [ ] Performance panel shows no layout/paint per frame for the animation.

## Checked

2026-10-28. Confirmed in the MDN @keyframes, animation and easing-function pages: shorthand order, animation-fill-mode, iteration-count and direction, steps() and linear() easing functions, comma-separated multiple animations. Removed: the engine-support claim, the restart-by-same-name claim, the animationend edge-case details and the compositor-only performance claim.

Method: documentation only; no commands were run.
