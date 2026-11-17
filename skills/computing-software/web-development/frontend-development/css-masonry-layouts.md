---
id: computing-software.web-development.frontend-development.css-masonry-layouts
name: css-masonry-layouts
category: computing-software
field: web-development
product: frontend-development
tags: [css-masonry, grid-lanes, masonry-layout, css-grid]
level: advanced
status: docs-checked
description: "Building masonry layouts: the CSS grid-lanes / masonry proposal status, progressive enhancement, column and JavaScript fallbacks, reading-order and lazy-loading pitfalls."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout/Grid_lanes
  - https://drafts.csswg.org/css-grid-3/
  - https://github.com/mdn/browser-compat-data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Masonry layouts

## 1. Native status
Level 3 of the CSS grid layout specification defines grid lanes layout (often called masonry) through `display: grid-lanes` and `inline-grid-lanes`. MDN marks it experimental, and browser-compat-data lists support only in Safari 26.4 (none in Chrome or Firefox). Treat it as progressive enhancement and feature-detect:
```css
.gallery { display: grid; grid-template-columns: repeat(auto-fill, minmax(14rem, 1fr)); gap: 1rem; }
@supports (display: grid-lanes) {
  .gallery { display: grid-lanes; }   /* each item goes into the lane with the most room */
}
```
The plain grid fallback is acceptable: aligned rows with uneven gaps under short items.

## 2. CSS-only fallbacks
- **Multicol**: `columns: 14rem; column-gap: 1rem;` with `break-inside: avoid` on items. Order runs down each column, so newest-first feeds read wrong.
- **Grid with row spans**: tiny row tracks (`grid-auto-rows: 8px`) and per-item `grid-row-end: span N` computed from height (needs JS to measure, but layout is native).

## 3. JavaScript fallback
A few lines of script: put items in N columns by adding each to the currently shortest. Recalculate on `ResizeObserver` and after each image `load` (or reserve space with `width`/`height` attributes so heights are known up front).

## 4. Pitfalls
- **Reading order**: tab and screen-reader order follows the DOM; masonry visually scatters it. Use this layout for content where order matters little (galleries).
- **Layout shifts**: images without dimensions reflow the whole wall as they load - always set `width`/`height` or `aspect-ratio`.
- **Infinite scroll**: appending items should not reposition existing ones; test this with whichever technique you use.

## Verify
- [ ] Fallback grid looks acceptable in browsers without support; no CLS as images load; keyboard order is sensible.

## Checked

Checked 2026-10-26 against current documentation. MDN grid lanes guide (`display: grid-lanes` and `inline-grid-lanes`, packing into the lane with most room, spanning and positioned items) and browser-compat-data (Safari 26.4 only; Chrome and Firefox none; no `grid-template-rows: masonry` entry remains). Removed the old `masonry` branch, the named JavaScript libraries and the unconfirmed 2025 CSSWG history.

Method: documentation only; no commands were run.
