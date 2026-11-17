---
id: computing-software.web-development.responsive-design.responsive-images-and-art-direction
name: responsive-images-and-art-direction
category: computing-software
field: web-development
product: responsive-design
tags: [responsive-images, picture-element, art-direction, aspect-ratio, object-fit, media-queries, layout, responsive-design, web-development]
level: advanced
status: verified
description: "Art direction with <picture> (swapping crop/composition per breakpoint, not just resolution) and layout-driven image sizing with object-fit."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Responsive_images
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Responsive images — art direction, not just resolution switching

**Goal:** know the difference between serving the *same* image at a smaller size
(resolution switching, `srcset`/`sizes`) and serving a *differently cropped*
image per layout (art direction, `<picture>` + `media`) — they solve different
problems and conflating them produces either bloated files or bad crops.

## 1. Resolution switching vs art direction — different tool, different problem
- **Resolution switching** (`srcset`/`sizes`, covered in the web-performance
  image skill): same composition, different pixel dimensions, browser picks
  based on viewport/DPR (run: with `sizes="(min-width: 64em) 30vw, (min-width: 40em) 45vw, 92vw"` and 400/600/900/1200w candidates, a 390px viewport chose 400w at DPR 1 and 900w at DPR 2, an 800px viewport chose 400w, 1440px chose 600w). Use when the image looks fine cropped the same way at
  every size — a product photo, a portrait.
- **Art direction** (`<picture>` + `<source media="...">`): genuinely different
  crops/compositions per breakpoint — a wide landscape hero on desktop that
  would lose its subject entirely if just scaled down, replaced by a tighter
  portrait-oriented crop on mobile.
```html
<picture>
  <source media="(max-width: 600px)" srcset="hero-mobile-crop.jpg">
  <source media="(min-width: 601px)" srcset="hero-desktop-wide.jpg">
  <img src="hero-desktop-wide.jpg" alt="Team celebrating a product launch">
</picture>
```
Using `<picture>` purely for resolution switching (same crop, different sizes)
works (run: sources with `max-width: 600px` and `min-width: 601px` switched exactly at 600/601px) but is the wrong tool — it's heavier to author and maintain than
`srcset`/`sizes` for that case; reserve `<picture>` for when the crop itself
needs to change.

## 2. `object-fit`/`object-position` — fitting an image into a fixed box
```css
.avatar { width: 48px; height: 48px; object-fit: cover; object-position: top; }
```
`object-fit: cover` fills the box without distortion by cropping overflow
(like CSS `background-size: cover` but for a real `<img>`, which keeps it
accessible and lazy-loadable unlike a background image). `object-position`
controls which part of the image stays visible when cropped — critical for
portraits where the default center-crop cuts off a face; set it per-image
or make it a CMS-editable "focal point" field for user-uploaded content
rather than guessing one fixed value for all images.

## 3. Choosing breakpoints for art direction based on content, not devices
Pick the breakpoint where the *image itself* needs to change, not where a
device class changes — a landscape hero might need the mobile crop at
600px while the rest of the page's media queries switch at 768px; these
don't have to match. Test real content at the actual breakpoint, not just a
generic device preset, since a crop that works for one photo's composition
may clip a different photo's subject at the same width.

## 4. Common mistakes
- Setting a `max-width: 100%` on `<img>` without `height: auto` — distorts
  aspect ratio on resize instead of scaling proportionally (run: a 600x400 image with `width`/`height` attributes in a 300px page rendered 300x400 without `height: auto` and 300x200 with it).
- Art-directing with CSS `background-image` + media queries instead of
  `<picture>` — loses the image from the accessibility tree (no `alt`) and
  native lazy-loading.
- Not providing an `alt` that matches the art-directed version — if the mobile
  crop removes a person from frame, the alt text should still describe what's
  meaningfully visible in whichever version actually renders, written to cover
  the closest common description if that's impractical to vary.
- Forgetting `sizes` still matters *within* each `<picture>` `<source>` if that
  source itself also has multiple resolution candidates — art direction and
  resolution switching combine, they aren't mutually exclusive.

## Verify
- [ ] `<picture>` is used only where the crop/composition genuinely changes per breakpoint, not as a `srcset` substitute.
- [ ] Breakpoints for art-directed swaps are chosen by testing the actual image, not copied from the page's layout breakpoints.
- [ ] `object-position` is set deliberately (or CMS-editable) wherever `object-fit: cover` could crop out the subject.
- [ ] Every `<img>` with a fixed width also constrains height proportionally (`height: auto` or `aspect-ratio`).
- [ ] No art-directed image is implemented as a CSS `background-image` where a real `<img>`/`<picture>` would preserve accessibility and lazy-loading.
