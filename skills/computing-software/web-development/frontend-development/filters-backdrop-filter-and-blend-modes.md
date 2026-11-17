---
id: computing-software.web-development.frontend-development.filters-backdrop-filter-and-blend-modes
name: filters-backdrop-filter-and-blend-modes
category: computing-software
field: web-development
product: frontend-development
tags: [backdrop-filter, mix-blend-mode, css-filter, drop-shadow, isolation, frosted-glass]
level: practitioner
status: docs-checked
description: "Using filter, backdrop-filter and blend modes: frosted glass, drop-shadow vs box-shadow, stacking context and fixed-position side effects, isolation, performance and contrast."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/filter
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/backdrop-filter
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/mix-blend-mode
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Display/Containing_block
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Positioned_layout/Stacking_context
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Filters, backdrop-filter and blend modes

## 1. filter
```css
.disabled { filter: grayscale(1) opacity(.6); }
.icon     { filter: drop-shadow(0 2px 4px rgb(0 0 0 / .3)); }   /* follows the PNG/SVG alpha shape */
.hover:hover { filter: brightness(1.1); }
```
`drop-shadow()` traces transparency (icons, cut-out images); `box-shadow` draws the rectangle.

## 2. Frosted glass
```css
.toolbar {
  background: rgb(255 255 255 / .6);
  -webkit-backdrop-filter: blur(12px) saturate(1.4);   /* older Safari */
  backdrop-filter: blur(12px) saturate(1.4);
}
@supports not (backdrop-filter: blur(1px)) { .toolbar { background: rgb(255 255 255 / .95); } }
```
Needs a translucent background to show anything. Text contrast varies with whatever scrolls behind: test over busy images or raise background opacity.

## 3. Side effects (common bugs)
Any `filter` or `backdrop-filter` other than `none`:
- creates a **stacking context** (z-index of children is now local);
- becomes the **containing block for `position: fixed` descendants**: a fixed modal inside a filtered parent scrolls with it and is clipped. Move overlays to `<body>`/top layer (`<dialog>`, popover).

## 4. Blend modes
```css
.duotone img { mix-blend-mode: multiply; }      /* image blends with the coloured parent background */
.card { isolation: isolate; }                    /* limit blending to this card */
.hero { background: url(a.jpg), linear-gradient(#4f46e5, #ec4899); background-blend-mode: overlay; }
.cursor { mix-blend-mode: difference; }          /* always-visible inverse cursor/text */
```
`isolation: isolate` (or any new stacking context) stops a child blending with content behind the parent.

## Verify
- [ ] Fixed-position children of filtered elements behave; frosted bars keep 4.5:1 contrast over the busiest content.

## Checked

Checked 2026-10-26 against current documentation. MDN `backdrop-filter` (needs a transparent or partially transparent element), `mix-blend-mode` (blends within the stacking context), containing-block guide (`filter`/`backdrop-filter` create a containing block for fixed descendants) and stacking-context guide (`filter` creates a stacking context); `backdrop-filter` unprefixed from Safari 18. Removed unconfirmed performance claims.

Method: documentation only; no commands were run.
