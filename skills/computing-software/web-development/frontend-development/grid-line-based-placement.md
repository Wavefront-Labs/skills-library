---
id: computing-software.web-development.frontend-development.grid-line-based-placement
name: grid-line-based-placement
category: computing-software
field: web-development
product: frontend-development
tags: [grid-line-placement, grid-named-lines, grid-column, grid-span, full-bleed-layout, css-grid]
level: practitioner
status: docs-checked
description: "Placing items on CSS Grid lines: start/end and span syntax, negative line numbers, named lines and the full-bleed content pattern, overlapping items and implicit tracks."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout/Line-based_placement
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout/Named_grid_lines
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grid line-based placement

## 1. Syntax
```css
.item { grid-column: 2 / 4; }          /* from line 2 to line 4 (spans 2 tracks) */
.item { grid-column: 2 / span 3; }     /* start at 2, span 3 tracks */
.item { grid-column: span 2; }         /* auto-placed, 2 wide */
.item { grid-column: 1 / -1; }         /* first to last EXPLICIT line: full width */
.item { grid-area: 1 / 1 / 3 / 4; }    /* row-start / col-start / row-end / col-end */
```
Lines are numbered from 1; negative numbers count from the end of the **explicit** grid only, so `1 / -1` does not cover implicit columns.

## 2. Named lines: full-bleed article layout
```css
.article {
  display: grid;
  grid-template-columns:
    [full-start] minmax(1rem, 1fr)
    [content-start] minmax(0, 65ch) [content-end]
    minmax(1rem, 1fr) [full-end];
}
.article > * { grid-column: content; }        /* "content" uses content-start / content-end */
.article > .bleed { grid-column: full; }      /* images/quotes break out edge to edge */
```
Lines named `foo-start`/`foo-end` create an implicit area `foo`.

## 3. Overlap
Items can share cells: place a caption over an image with the same `grid-area` and control order with `z-index` (grid items honour z-index without `position`).
```css
.hero { display: grid; } .hero > * { grid-area: 1 / 1; }
.hero .caption { align-self: end; z-index: 1; }
```
This replaces most absolute-positioning overlays and keeps the container sized to the tallest child.

## 4. Implicit tracks
Placing an item at `grid-column: 5` in a 3-column grid creates implicit columns 4-5 sized by `grid-auto-columns`. Auto-placed items flow around explicitly placed ones; use `grid-auto-flow: dense` only when visual order may differ from DOM order.

## Gotchas
- Visual reordering with line placement does not change tab/reading order (WCAG 1.3.2); keep DOM order meaningful.

## Verify
- [ ] DevTools grid overlay with "show line names" confirms items sit on the intended lines at each breakpoint.

## Checked
2026-10-26. MDN line-based placement and named grid lines guides (main, 2026-10-26): confirmed -1 addresses the last line of the explicit grid only, named lines such as content-start/content-end, and implicit grid areas from named lines. Removed the unconfirmed grid-template-areas reverse claim, the span-with-name gotcha and the unread blog source.
Method: documentation only; no commands were run.
