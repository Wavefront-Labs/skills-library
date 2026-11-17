---
id: creative-arts.design-for-form-and-experience.interaction-design.building-column-grids-and-gutters
name: building-column-grids-and-gutters
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [column-grid, layout-grid, gutters, grid-system, responsive-grid, ui-layout, visual-hierarchy]
level: practitioner
status: draft
description: "Build UI column grids: choose 12/8/4 columns, gutters and margins per breakpoint, align components to the grid, and set it up as layout grids in Figma and CSS."
sources:
  - "Material Design 3 - Layout: Understanding layout, columns and gutters (m3.material.io/foundations/layout)"
  - "Josef Muller-Brockmann, Grid Systems in Graphic Design (Niggli, 1981)"
  - "MDN Web Docs - CSS grid layout (developer.mozilla.org/docs/Web/CSS/CSS_grid_layout)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Column grids and gutters

**Goal:** a layout structure that makes alignment automatic and adapts across screen sizes.

## Choose the grid
- **Columns:** 12 on desktop (divisible by 2, 3, 4, 6), 8 on tablet, 4 on mobile (Material 3 uses 4/8/12). Fewer columns on small screens, not smaller ones.
- **Gutters:** the gap between columns; typically 16-24 px on mobile and tablet, 24-32 px on desktop.
- **Margins:** outer space; 16 px phone, 24-32 px tablet, centred max-width container on desktop (1120-1440 px) so line length stays sane.
- Choose **fixed, fluid or hybrid**: fluid columns with a max-width container is the usual default.

## Setting up
- **Figma:** frame, Layout grid (Ctrl+Shift+4), Columns; count, gutter, margin, type (stretch or fixed). Create variants per breakpoint (360, 768, 1280) and save as a Grid style.
- **CSS:** `display:grid; grid-template-columns: repeat(12, 1fr); column-gap: 24px; max-width: 1280px; margin-inline: auto;`; or use `repeat(auto-fit, minmax(16rem, 1fr))` for card grids.
- Add an **8-pt (or 4-pt) baseline/spacing system** so vertical rhythm matches horizontal.

## Using it
- Components snap to columns (a card spans 4 of 12 on desktop, 4 of 8 tablet, 4 of 4 mobile).
- Content (text, images) aligns to column edges; backgrounds can bleed to the frame.
- Mixed spans create hierarchy (an 8-column article plus a 4-column sidebar).
- Check alignment across screens; deviations should be deliberate.

## Verify
- [ ] Column count, gutter and margin defined per breakpoint.
- [ ] Components span whole columns; max container width limits line length.
- [ ] Grid exists as a style in the design file and as tokens in code.
