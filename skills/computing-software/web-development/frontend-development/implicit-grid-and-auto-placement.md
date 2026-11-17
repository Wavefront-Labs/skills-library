---
id: computing-software.web-development.frontend-development.implicit-grid-and-auto-placement
name: implicit-grid-and-auto-placement
category: computing-software
field: web-development
product: frontend-development
tags: [css-grid, grid-auto-flow, implicit-grid, auto-placement, dense-packing, css]
level: practitioner
status: docs-checked
description: "Controlling CSS grid auto-placement and implicit tracks: grid-auto-rows/columns, auto-flow dense, spanning items, explicit vs implicit lines and the dense reading-order trap."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout/Auto-placement
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/grid-auto-flow
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout/Grid_lanes
  - https://www.w3.org/TR/css-grid-2/#auto-placement-algo
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Implicit grid, auto-flow and placement

## 1. Explicit vs implicit
`grid-template-*` defines explicit tracks. Items placed beyond them (or more items than cells) create **implicit** tracks sized by `grid-auto-rows` / `grid-auto-columns` (default `auto`).
```css
.gallery { display: grid; grid-template-columns: repeat(4, 1fr); grid-auto-rows: minmax(10rem, auto); gap: .5rem; }
```

## 2. Auto-placement
- `grid-auto-flow: row` (default) fills row by row; `column` fills columns (combine with `grid-auto-columns` and `grid-template-rows`).
- Spanning: `.feature { grid-column: span 2; grid-row: span 2; }`.
- Placing some items explicitly (`grid-column: 1 / -1`) and letting others auto-flow around them works; explicitly placed items go first.
- `-1` refers to the last **explicit** line; it does not reach into implicit tracks.

## 3. dense
```css
.gallery { grid-auto-flow: row dense; }
```
Backfills holes left by large spanning items. Visual order then differs from DOM order - focus/reading order jumps around (WCAG 1.3.2/2.4.3). Use only for non-interactive, order-insensitive content (photo walls), never for lists users read or tab through.

## 4. Masonry
Masonry is specified as `display: grid-lanes`, which MDN marks experimental; until it is widely supported use `column-count`, a script library, or accept aligned rows.

## 5. Placement tips
- Overlap items in the same cell for layered hero designs: give both `grid-area: 1 / 1`.
- `order` changes placement order with the same a11y caveat as dense.

## Verify
DevTools grid overlay shows implicit tracks (dashed lines) - check none are created unexpectedly; Tab order matches visual order unless content is non-interactive.

## Checked
2026-10-26. MDN auto-placement guide, grid-auto-flow page and grid lanes page (main, 2026-10-26): confirmed grid-auto-flow accepts row, column, dense, row dense and column dense, dense backfills holes, -1 reaches only the explicit grid, and masonry is the experimental display: grid-lanes. Removed the unconfirmed named-areas bullet and the old grid-template-rows: masonry spelling.
Method: documentation only; no commands were run.
