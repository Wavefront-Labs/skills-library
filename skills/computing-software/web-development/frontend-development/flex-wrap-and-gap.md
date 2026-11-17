---
id: computing-software.web-development.frontend-development.flex-wrap-and-gap
name: flex-wrap-and-gap
category: computing-software
field: web-development
product: frontend-development
tags: [flexbox, flex-wrap, gap, responsive-layout, css]
level: practitioner
status: docs-checked
description: "Building wrapping layouts with flex-wrap and gap: intrinsic responsive rows without media queries, flex-basis thresholds, last-row behaviour, and when grid is better."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/flex-wrap
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/gap
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/align-content
  - https://github.com/mdn/browser-compat-data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flex wrapping and gap

## 1. Basics
```css
.tags { display: flex; flex-wrap: wrap; gap: .5rem .75rem; }   /* row-gap column-gap */
```
Flex `gap` is supported from Chrome 84, Firefox 63 and Safari 14.1 (browser-compat-data). Replaces negative-margin hacks.

## 2. Intrinsic responsive rows (no media queries)
```css
.cluster { display: flex; flex-wrap: wrap; gap: 1rem; }
.cluster > * { flex: 1 1 16rem; }        /* items grow, wrap when narrower than 16rem */
```
"Switcher": all items side by side above a threshold, all stacked below:
```css
.switcher { display: flex; flex-wrap: wrap; gap: 1rem; }
.switcher > * { flex-grow: 1; flex-basis: calc((40rem - 100%) * 999); }
```

## 3. Last-row behaviour
With `flex: 1 1 16rem`, the last row's items stretch to fill (a lone item becomes full width). If you need a consistent column grid where the last row aligns with the others, use grid (`repeat(auto-fill, minmax(16rem, 1fr))`). Flex wrap is for content-sized things: tags, buttons, toolbars, form rows.

## 4. Gotchas
- `flex-wrap` defaults to `nowrap`: items shrink and overflow instead of wrapping.
- `align-content` controls spacing between wrapped lines (default `normal` = stretch).
- Wrapped toolbars: keep DOM order = visual order for keyboard users; avoid `flex-direction: row-reverse` / `order` reshuffles (WCAG 1.3.2, 2.4.3).
- `wrap-reverse` flips the cross axis - rarely what you want.

## Verify
Resize from 320px to wide: items wrap without overflow; Tab order matches visual order.

## Checked

Checked 2026-10-26 against current documentation. MDN `flex-wrap`, `gap` and `align-content` (no effect on single-line containers) and browser-compat-data for flex `gap` (Chrome 84, Firefox 63, Safari 14.1). The switcher `flex-basis: calc((40rem - 100%) * 999)` arithmetic was checked by reasoning (negative below clamps to 0, large positive above forces wrapping).

Method: documentation only; no commands were run.
