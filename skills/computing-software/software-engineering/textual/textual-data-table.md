---
id: computing-software.software-engineering.textual.textual-data-table
name: textual-data-table
category: computing-software
field: software-engineering
product: textual
tags: [textual, widgets-data-table, data-table, table, cursors, sorting, keys, tui]
level: practitioner
status: docs-checked
description: "Build and update a Textual DataTable: add columns and rows with keys, cursor types and messages, remove data, fixed rows and columns, sorting and row labels."
sources: [https://textual.textualize.io/widgets/data_table/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual DataTable

Goal: display, navigate and modify tabular data.

## Method
- Add data: `add_columns("lane", "swimmer", ...)` then `add_rows(rows)`; singly with `add_column` and `add_row`. Cells may be strings or Rich renderables such as `Text` for styling and justification.
- Keys: `add_row(..., key=...)` and `add_column(..., key=...)` take a unique key (use a database primary key); without one Textual generates it and `add_row` returns it. Use keys, not coordinates, because deletion and sorting move cells. `coordinate_to_cell_key(coord)` converts a coordinate to `(row_key, column_key)`.
- Cursor: `cursor_type` is `"cell"` (default), `"row"`, `"column"` or `"none"`; `cursor_coordinate` holds the position, `hover_coordinate` the mouse position. Arrow keys, Page Up/Down, Home, End move the highlight (`CellHighlighted`); Enter selects (`CellSelected`). With row or column cursor the `Row*` or `Column*` equivalents are sent. Clicking sends highlighted then selected. Other messages: `HeaderSelected`, `RowLabelSelected`.
- Update: `update_cell` (by keys) and `update_cell_at` (by coordinate).
- Remove: `clear()`, `remove_row(key)`, `remove_column(key)`. Row under the cursor:

```python
row_key, _ = table.coordinate_to_cell_key(table.cursor_coordinate)
table.remove_row(row_key)
```

- Fixed data: assign ints to `fixed_rows` and `fixed_columns` to pin top rows and left columns while scrolling.
- Sorting: `sort("country", "region")` sorts by columns (ColumnKey or the key given to `add_column`); `sort(key=fn)` calls `fn` once per row with a tuple of all values; `sort("hours", "rate", key=lambda h, r: h*r)` passes just those columns. `reverse=True` reverses.
- Labels: pass a label to `add_row` for a left column the cursor cannot enter (`show_row_labels`, default `True`).
- Other reactives: `show_header` (True), `zebra_stripes` (False), `header_height` (1), `show_cursor` (True).

## Gotchas
- If cells are formatted text, your sort key function must undo the formatting for correct ordering.

## Verify
The docs example adds columns `lane`, `swimmer`, `country`, `time`, then rows; `cursor_coordinate` starts at `Coordinate(0, 0)`.

## Checked

2026-11-07: every claim was read against the full text of these pages: widgets/data_table. Nothing needed removing.

Method: documentation only; no commands were run.
