---
id: computing-software.web-development.tailwind-css.prefers-reduced-motion
name: prefers-reduced-motion
category: computing-software
field: web-development
product: tailwind-css
tags: [css-animations, css-transitions, prefers-reduced-motion, reduced-motion, vestibular-disorders, motion-accessibility, animation-from-interactions]
level: practitioner
status: verified
description: "Respecting prefers-reduced-motion in CSS and JS: no-motion-first patterns, replacing movement with fades, scroll and parallax handling, and testing."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
  - https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html
  - https://web.dev/articles/prefers-reduced-motion
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# prefers-reduced-motion

**Goal:** users who ask their OS for reduced motion (vestibular disorders, migraines, distraction) don't get parallax, zooms and large movement.

## 1. CSS: motion as an enhancement
```css
.card { transition: opacity 150ms; }                     /* safe default */
@media (prefers-reduced-motion: no-preference) {
  .card { transition: opacity 150ms, transform 300ms; }
  .card:hover { transform: translateY(-4px); }
  html { scroll-behavior: smooth; }
}
```
"No-motion-first" (add motion inside `no-preference`) is safer than removing it in `reduce`, because new animations default to off for those users.

Global safety net (blunt, use with care - it also kills spinners' meaning):
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; scroll-behavior: auto !important; }
}
```
Using 0.01 ms rather than `none` keeps `animationend`/`transitionend` firing for code that waits on them (run in Chromium 156: both events fired with the safety-net rule applied).

## 2. Reduce, don't remove
Replace movement with opacity/colour changes: a slide-in toast becomes a fade. Loading spinners can keep a slower or non-rotating indicator; essential motion (progress) stays.

## 3. JavaScript
```js
const mq = matchMedia('(prefers-reduced-motion: reduce)');
const reduce = () => mq.matches;
mq.addEventListener('change', () => updateAnimations());
el.animate(frames, { duration: reduce() ? 0 : 400 });
scrollIntoView({ behavior: reduce() ? 'auto' : 'smooth' });
```
Animation libraries: Framer Motion `useReducedMotion()` / `MotionConfig reducedMotion="user"` (the Motion docs say this disables transform and layout animations but keeps opacity and colour ones); GSAP `gsap.matchMedia()`; Lottie - show a static frame.

## 4. WCAG
2.3.3 Animation from Interactions (AAA): motion triggered by interaction can be disabled. 2.2.2 Pause, Stop, Hide (A): auto-playing motion > 5 s needs a pause control regardless of OS setting. Offer an in-app motion toggle for users who don't know the OS setting.

## Verify
- [ ] With OS reduced motion on (or DevTools > Rendering > Emulate prefers-reduced-motion), no parallax, slides or zooms remain.
- [ ] Toggling the setting live updates JS-driven animations.
- [ ] Carousels/auto-playing media still have pause controls.
