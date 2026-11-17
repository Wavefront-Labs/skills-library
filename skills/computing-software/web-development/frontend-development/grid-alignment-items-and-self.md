---
id: computing-software.web-development.frontend-development.grid-alignment-items-and-self
name: grid-alignment-items-and-self
category: computing-software
field: web-development
product: frontend-development
tags: [grid-alignment, justify-items, align-self, place-items, css-grid, box-alignment]
level: practitioner
status: docs-checked
description: "Aligning items inside CSS grid cells with justify-items, align-items, justify-self, align-self and place-items: stretch defaults, centring, baseline alignment and overflow."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout/Box_alignment
  - https://www.w3.org/TR/css-align-3/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grid alignment: justify-items, align-self, place-items

Grid has two axes of alignment for items within their grid area: **inline** (`justify-*`) and **block** (`align-*`). Unlike flexbox, `justify-items/self` work in grid.

## 1. Container-level defaults
```css
.cards { display: grid; grid-template-columns: repeat(3, 1fr); align-items: start; }   /* stop stretching heights */
.icons { display: grid; place-items: center; }                                          /* align-items + justify-items */
```
- Default is `stretch` on both axes: items fill the cell (unless they have a fixed size or aspect ratio). That is why cards in a row are equal height - usually wanted.
- `align-items: start` lets each card take its own height.
- `place-items: center` on a single-cell grid is the shortest centring recipe.

## 2. Per-item overrides
```css
.badge { justify-self: end; align-self: start; }   /* top-right corner of its cell */
.cta   { place-self: center; }
```

## 3. Images and replaced elements
Items with an intrinsic aspect ratio, such as images, behave as `start` instead of stretching. Use `width: 100%; height: 100%; object-fit: cover` for full-bleed cell images.

## 4. Baseline alignment
`align-items: baseline` aligns first text baselines across a row (useful for label/value lists with different font sizes). `last baseline` aligns the last lines - footers of cards.

## 5. Common confusion
| Want | Use |
|---|---|
| Move the whole grid within a larger container | `justify-content` / `align-content` |
| Move items inside their cells | `justify-items` / `align-items` / `*-self` |
| Space between tracks | `gap`, not `justify-content: space-between` |


## 6. Subgrid cards
To align card internals (title, body, footer) across a row, use `grid-template-rows: subgrid` on cards spanning 3 rows; alignment then applies per shared row.

## Verify
- [ ] Items sit where designed at every breakpoint; equal-height behaviour is intentional; centred content doesn't clip when larger than its cell.

## Checked
2026-10-26. MDN grid box alignment guide (main, 2026-10-26): confirmed the default is stretch except for items with an intrinsic aspect ratio, which behave as start, and that justify-* works in grid. Removed the unconfirmed safe-centre sentence and the unread justify-items source.
Method: documentation only; no commands were run.
