---
id: computing-software.software-engineering.textual.textual-layout-grid
name: textual-layout-grid
category: computing-software
field: software-engineering
product: textual
tags: [textual, layout, grid, grid-size, grid-columns, grid-rows, column-span, gutter]
level: practitioner
status: docs-checked
description: "Build Textual grid layouts with grid-size, grid-columns, grid-rows, row-span, column-span and grid-gutter, including auto-created rows."
sources: [https://textual.textualize.io/guide/layout/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual grid layout

Goal: arrange widgets in cells that can have custom sizes, spans and spacing. Textual grid has little in common with browser CSS Grid.

## Method

1. Set `layout: grid;` and `grid-size` on the container. `grid-size: 3 2;` is 3 columns by 2 rows. Widgets fill cells left to right, top to bottom.
2. A seventh widget in a 3x2 grid is not visible (no cell). Omit the row count, `grid-size: 3;`, and rows are created on demand.
3. Column widths: `grid-columns`, one value per column, for example `grid-columns: 2fr 1fr 1fr;` (first column twice as wide). Row heights: `grid-rows`, for example `grid-rows: 25% 75%;`.
4. If fewer values are given than columns or rows, they repeat: with `grid-size: 4;`, `grid-columns: 2 4;` equals `2 4 2 4`; with three columns it equals `2 4 2`.
5. `auto` can replace any dimension (`grid-columns: auto 1fr 1fr;`) to size from content; it adjusts when content changes.
6. Spans: give the widget an ID in `compose` and target it in CSS, for example:

```css
#two {
    column-span: 2;
    row-span: 2;
}
```

The cell expands right (columns) and down (rows); later widgets shift along and may wrap to a new row. A column-span larger than the remaining columns has the same effect as the maximum available.

7. Spacing: `grid-gutter: 1;` on the grid container (not on child cells). Two values set vertical and horizontal gutter; `grid-gutter: 1 2;` is common because terminal cells are about twice as tall as wide.

## Gotchas

- Gutter applies only between cells, not between cells and the container edge.
- `grid-gutter` must be set on the widget with `layout: grid`.

## Verify

Run the app with `grid-size: 3;` and seven children: a third row appears holding the seventh widget.

## Checked

2026-11-07: every claim was read against the full text of these pages: guide/layout. Nothing needed removing.

Method: documentation only; no commands were run.
