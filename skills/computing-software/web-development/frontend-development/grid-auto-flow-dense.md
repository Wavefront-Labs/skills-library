---
id: computing-software.web-development.frontend-development.grid-auto-flow-dense
name: grid-auto-flow-dense
category: computing-software
field: web-development
product: frontend-development
tags: [grid-auto-flow-dense, grid-auto-flow, auto-placement, css-grid, focus-order]
level: practitioner
status: docs-checked
description: "Using grid-auto-flow dense to backfill holes in auto-placed grids, how it reorders items visually, when that breaks reading and focus order, and safer alternatives."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/grid-auto-flow
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/reading-flow
  - https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html
  - https://github.com/mdn/browser-compat-data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# grid-auto-flow: dense and source order

## 1. What it does
```css
.gallery { display: grid; grid-template-columns: repeat(auto-fill, minmax(10rem, 1fr));
           grid-auto-rows: 10rem; grid-auto-flow: row dense; gap: .5rem; }
.wide { grid-column: span 2; }
.tall { grid-row: span 2; }
```
With the default `row` (sparse) algorithm, an item that doesn't fit leaves a hole and later items continue after it. `dense` goes back and fills earlier holes with later items that fit, so items appear out of DOM order.

## 2. Acceptable uses
- Image galleries or tag grids where each item is independent and order carries no meaning.
- Dashboards of tiles where users don't navigate sequentially (still verify keyboard flow).

## 3. When it breaks things
- Tab order and screen-reader order follow the DOM, so a keyboard user jumps from tile 3 (top-right) to tile 4 (bottom) back to tile 5 (filled hole top-left) - WCAG 2.4.3 failure if the items are interactive and sequence matters.
- Chronological feeds, ranked results, steps: never use dense.

## 4. Alternatives
- Choose spans that tile cleanly (e.g. wide items only at known positions) so sparse flow leaves no holes.
- Explicit placement with `grid-template-areas` for designed layouts.
- Sort the data server-side to fill rows (a packing pass) so DOM order matches visual order.
- `reading-flow: grid-rows` (Chrome 137; no Firefox or Safari support in browser-compat-data) makes focus follow visual order; progressive enhancement only.

## 5. Column flow
`grid-auto-flow: column dense` fills down columns; combine with `grid-template-rows` and `grid-auto-columns`. Same order caveats.

## Verify
- [ ] Holes filled visually; Tab through interactive items and compare with visual order; order-sensitive lists use sparse flow.

## Checked

Checked 2026-10-26 against current documentation. MDN `grid-auto-flow` and `reading-flow` (values `grid-rows`, `grid-columns`, `source-order`; Chrome 137 only) and browser-compat-data for `dense` (Chrome 57, Firefox 52, Safari 10.1). Removed an unreachable blog source.

Method: documentation only; no commands were run.
