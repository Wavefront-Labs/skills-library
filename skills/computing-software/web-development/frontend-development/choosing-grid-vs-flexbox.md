---
id: computing-software.web-development.frontend-development.choosing-grid-vs-flexbox
name: choosing-grid-vs-flexbox
category: computing-software
field: web-development
product: frontend-development
tags: [css-grid, grid-vs-flexbox, flexbox, layout, css]
level: practitioner
status: docs-checked
description: "Deciding between CSS grid and flexbox: one vs two dimensions, content-out vs layout-in sizing, decision table for common components, and combining them."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout/Relationship_with_other_layout_methods
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Flexible_box_layout/Relationship_with_other_layout_methods
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout/Subgrid
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing grid vs flexbox

## 1. The core difference
- **Flexbox: content out.** Items size from their content; space is distributed along one axis; each line is independent.
- **Grid: layout in.** You define tracks; items snap to them in two dimensions; columns align across rows.
If you need things to align in both rows and columns, use grid. If you need a row (or column) of variable-size things, use flex.

## 2. Decision table
| Component | Choice | Why |
|---|---|---|
| Navbar, toolbar, button group, tag list | flex (+ wrap) | one axis, content-sized items, `margin-inline-start: auto` splits |
| Card gallery with equal columns | grid `auto-fill minmax` | last row aligns to columns |
| Page shell (header/sidebar/main/footer) | grid areas | 2D, named regions, responsive re-arrangement |
| Form with label column | grid (+ subgrid) | label column aligns across fields |
| Media object, input group | flex | content-sized + one growing item |
| Centring one thing | either (`place-items: center` is shortest) | |
| Overlapping layers (text over image) | grid same-cell stacking | no absolute positioning needed |
| Equal-height cards with aligned inner parts | grid + subgrid | flex can't align across cards |

## 3. Combine
Grid for macro layout, flex inside components. A grid item can be a flex container and vice versa.

## 4. Shared behaviour
Both support `gap` and the Box Alignment properties. A flex item will not shrink below its `min-content` size, so long content needs `min-width: 0`. Neither should reorder content away from DOM order for interactive elements.

## 5. Avoid
- Flex with `width: calc(33.33% - gap)` hacks to fake columns - that's grid.
- Grid for content-sized rows of chips with fixed columns - wastes space and wraps poorly.

## Verify
At narrow widths, check flex rows wrap naturally and grid columns collapse without overflow; DevTools overlays confirm intended structure.

## Checked
2026-10-26. MDN flexbox and grid relationship pages (main, 2026-10-26): confirmed flexbox is one-dimensional and grid two-dimensional, that a flex container does not line up items across lines (use grid), and that flex items shrink only down to min-content. Removed the unconfirmed grid minmax(0, 1fr) remark and the web.dev sources.
Method: documentation only; no commands were run.
