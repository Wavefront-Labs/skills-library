---
id: computing-software.web-development.responsive-design.breakpoints-fluid-layout-and-touch-targets
name: breakpoints-fluid-layout-and-touch-targets
category: computing-software
field: web-development
product: responsive-design
tags: [responsive-design, responsive-web-design, rwd, mobile-first, viewport-meta, media-queries, breakpoints, fluid-layout, fluid-typography, clamp, container-queries, cqi, srcset, sizes, picture-element, art-direction, responsive-images, touch-targets, tap-targets, hover-media-query, pointer-media-query, any-pointer, dvh, svh, lvh, viewport-units, safe-area-inset, device-testing, css-grid, flexbox, web-development, media-query-range-syntax, content-breakpoints, breakpoint-strategy]
level: practitioner
status: gated
description: "Responsive layouts: viewport meta, mobile-first, content-driven breakpoints, clamp() fluid type, container queries, srcset/sizes, 44-48px touch targets, pointer queries, dvh."
sources:
  - https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Responsive_Design
  - https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries
  - https://web.dev/learn/design
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Responsive_images
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Breakpoints, fluid layout and touch targets — fluid by default, breakpoints where content breaks

**Goal:** one codebase that reads well and is easy to operate from a 320px phone held in
one hand to a 2560px monitor, with any mix of touch, mouse and keyboard.

## 1. The non-negotiable baseline
```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```
Without it mobile browsers render a desktop-width layout and zoom out (gated: unconfirmed, source is paywalled or blocked). Never add `maximum-scale=1` or
`user-scalable=no` — MDN warns it prevents people with low vision from zooming, and WCAG requires at least 2x scaling.
```css
*, *::before, *::after { box-sizing: border-box; }
img, video, svg { max-width: 100%; height: auto; }
```

## 2. Mobile-first, content-driven breakpoints
Write the single-column small-screen layout with no media query, then add `min-width`
queries as space allows. Choose breakpoints by widening the browser until the **content**
looks wrong (line length over ~75 characters, cards stretched, nav wrapping) — not by
device models, which change every year. Use `em`/`rem` in media queries so they respond to
user font size: `@media (min-width: 48em) { … }`. Three or four breakpoints is usually enough.

Range syntax is widely supported now (Chrome 104, Firefox 102, Safari 16.4, Baseline 2023-03-27): `@media (48em <= width < 64em)` (run in Chromium 156).

## 3. Fluid first, fewer breakpoints
```css
.grid { display: grid; gap: 1rem;
        grid-template-columns: repeat(auto-fit, minmax(min(16rem, 100%), 1fr)); }
.wrap { width: min(100% - 2rem, 72rem); margin-inline: auto; }
h1   { font-size: clamp(1.75rem, 1.2rem + 2.5vw, 3rem); }
.section { padding-block: clamp(2rem, 5vw, 5rem); }
```
The `min(16rem, 100%)` stops overflow on very narrow screens. Always include a `rem` term in
fluid type (never pure `vw`): pure viewport units do not grow with browser zoom, and W3C lists incorrect use of viewport units to resize text as a failure of WCAG 1.4.4. Run: the `h1` clamp resolved to 28px at 320px, 35.2px at 640px and 48px at 1280px and 2560px; the `min(16rem, 100%)` grid had no horizontal overflow at 200px, while plain `minmax(16rem, 1fr)` overflowed to 256px.

## 4. Container queries for components
A card in a sidebar and in the main column should adapt to its slot, not the window.
```css
.card-slot { container-type: inline-size; }
@container (min-width: 30rem) { .card { display: grid; grid-template-columns: 10rem 1fr; } }
.card h3 { font-size: clamp(1rem, 4cqi, 1.5rem); }   /* cqi = 1% of container inline size */
```
Baseline newly available since 2023-02-14 (Chrome 105, Firefox 110, Safari 16). Use media queries for page layout,
container queries for components.

## 5. Responsive images
```html
<!-- Same image, different sizes: let the browser choose by width and DPR -->
<img src="card-600.jpg" alt="…" width="600" height="400" loading="lazy"
     srcset="card-400.jpg 400w, card-600.jpg 600w, card-900.jpg 900w, card-1200.jpg 1200w"
     sizes="(min-width: 64em) 30vw, (min-width: 40em) 45vw, 92vw">
<!-- Art direction / format fallback -->
<picture>
  <source media="(min-width: 48em)" srcset="hero-wide.avif" type="image/avif">
  <source srcset="hero-tall.avif" type="image/avif">
  <img src="hero-tall.jpg" alt="…" width="800" height="1000">
</picture>
```
`sizes` must describe the rendered width; a wrong or missing `sizes` (default `100vw`) makes
phones download desktop images. Keep `width`/`height` for aspect ratio (prevents layout shift).

## 6. Touch targets and input type
- Targets: aim for **44×44 CSS px** (WCAG 2.5.5 Target Size (Enhanced), Level AAA); Apple and Material guidance cite similar sizes (48 dp for Material) (gated: unconfirmed, source is paywalled or blocked). The Level AA minimum in WCAG 2.2 is 24×24 CSS px (2.5.8, with spacing and other exceptions). Grow the hit area with padding, not the icon.
- At least ~8px between adjacent targets.
- Detect capability, not screen size:
```css
@media (hover: hover) and (pointer: fine) { .row:hover .actions { opacity: 1; } }
@media (pointer: coarse) { .toolbar button { min-block-size: 48px; } }
```
Never hide essential actions behind hover: touch users can't hover (Chromium touch emulation: `(hover: hover)` false, `(pointer: coarse)` and `(any-pointer: coarse)` true; desktop Chromium matched `(hover: hover) and (pointer: fine)`), and a laptop with a touchscreen reports `any-pointer: coarse` too (gated: unconfirmed, source is paywalled or blocked).
- Inputs: `font-size` ≥ 16px stops iOS Safari zooming on focus (gated: unconfirmed, source is paywalled or blocked); use `type="email|tel|number"`
  and `inputmode`/`autocomplete` for the right keyboard.

## 7. Viewport height and safe areas
`100vh` on mobile equals the *largest* viewport (toolbar hidden), so full-height screens
get cut off (gated: unconfirmed, source is paywalled or blocked) (on desktop Chromium `100vh`, `100dvh` and `100svh` were all equal, 640px in a 640px window). Use `min-height: 100dvh` (dynamic), or `100svh` for the smallest stable size (dvh/svh/lvh: Chrome 108, Firefox 101, Safari 15.4).
For notched devices, add `viewport-fit=cover` to the meta tag (iOS 11 per the WebKit blog) and pad with
`env(safe-area-inset-bottom)` on fixed bottom bars (`env()` resolves to 0px on desktop Chromium).

## 8. Test on real devices
DevTools device mode is good for layout but does not reproduce real touch, mobile CPU,
on-screen keyboard or Safari quirks. Check at least one real iPhone (Safari) and one mid-range
Android (Chrome), in both orientations; use remote debugging (Safari Web Inspector,
`chrome://inspect`). Also test 320px width, 200% zoom and a large desktop.

## Verify
- [ ] Viewport meta present, zoom not disabled.
- [ ] No horizontal scroll at 320px; line length stays under ~75 characters on wide screens.
- [ ] Breakpoints in `em`/`rem`, placed where content broke.
- [ ] Fluid type mixes `rem` + `vw` and still scales with browser zoom.
- [ ] DevTools Network on a phone viewport shows appropriately small images.
- [ ] All tap targets ≥ 44px (≥ 24px minimum); nothing essential is hover-only.
- [ ] Full-height sections and bottom bars behave with the mobile toolbar showing and hidden.
