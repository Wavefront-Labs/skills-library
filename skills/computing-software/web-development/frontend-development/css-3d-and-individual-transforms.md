---
id: computing-software.web-development.frontend-development.css-3d-and-individual-transforms
name: css-3d-and-individual-transforms
category: computing-software
field: web-development
product: frontend-development
tags: [css-3d-transforms, individual-transform-properties, css-transforms, perspective, css-animation]
level: practitioner
status: docs-checked
description: "Using individual translate/rotate/scale properties and 3D transforms: composing transforms independently, perspective, preserve-3d, backface-visibility, card flips and pitfalls."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/translate
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/transform-style
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/perspective
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Display/Containing_block
  - https://drafts.csswg.org/css-transforms-2/#ctm
  - https://github.com/mdn/browser-compat-data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Individual transform properties and 3D transforms

## 1. Individual properties (Baseline 2022)
```css
.btn { translate: 0 0; scale: 1; rotate: 0deg; transition: scale .15s, translate .2s; }
.btn:hover { scale: 1.05; }
.btn:active { translate: 0 2px; }   /* doesn't clobber the hover scale */
```
- `translate`, `rotate`, `scale` animate independently; with `transform` a hover rule overrides the whole list and keyframes must repeat every function.
- Application order is fixed: `translate` -> `rotate` -> `scale` -> then `transform`. If you need a different order (rotate then translate for orbiting), use `transform`.
- `rotate: y 45deg` / `rotate: 1 1 0 30deg` for 3D axes; `scale: 1 1.2` per axis.

## 2. 3D basics
```css
.scene { perspective: 800px; perspective-origin: 50% 30%; }   /* on the parent: shared vanishing point */
.card  { transform-style: preserve-3d; transition: rotate .6s; }
.card.flipped { rotate: y 180deg; }
.face  { position: absolute; inset: 0; backface-visibility: hidden; }
.back  { rotate: y 180deg; }
```
- `perspective` on the parent gives siblings a common viewpoint; `transform: perspective(800px) rotateY(...)` on the element gives each its own.
- Smaller perspective (300px) = stronger distortion.
- `transform-style: preserve-3d` must be on every level between scene and faces; it is flattened by `overflow` other than `visible` or `clip`, `opacity < 1`, `filter`, `clip-path`, `mask-image`, `isolation: isolate`, `mix-blend-mode` other than `normal`, and `contain: paint`.

## 3. Performance and quality
- Every transformed element creates a stacking context and becomes the containing block for `position: fixed` descendants (common modal bug).

## 4. Accessibility
Large 3D rotations and parallax can trigger vestibular symptoms: wrap in `@media (prefers-reduced-motion: no-preference)` or swap to a fade.

## Verify
- [ ] Hover and active transforms compose without overriding; flip card hides back face in Safari and Chromium; reduced-motion users get a non-spatial alternative.

## Checked

Checked 2026-10-26 against current documentation. CSS Transforms Level 2 matrix algorithm (translate, rotate, scale, then `transform`), MDN `transform-style` grouping-property list, MDN containing-block guide (transform/filter/perspective create a containing block for fixed descendants), `perspective` page and `translate` support (Chrome 104, Firefox 72, Safari 14.1). Removed unconfirmed text-blur and `will-change` advice.

Method: documentation only; no commands were run.
