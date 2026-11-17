---
id: computing-software.general-digital-literacy.office-suites.rows-and-columns
name: rows-and-columns
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, spreadsheets, worksheets, rows-and-columns, insert-rows, hide-columns, unhide, column-width, autofit-column]
level: intro
status: docs-checked
description: "Insert, delete, resize, hide and unhide rows and columns in Excel, including AutoFit, unhiding column A and keeping hidden rows out of totals."
sources:
  - https://support.microsoft.com/en-us/accessibility/excel/keyboard-shortcuts-in-excel
  - https://support.microsoft.com/en-us/excel/get-started/insert-or-delete-rows-and-columns-in-excel
  - https://support.microsoft.com/en-us/excel/change-the-column-width-and-row-height
  - https://support.microsoft.com/en-us/excel/get-started/hide-or-show-rows-or-columns
  - https://support.microsoft.com/en-us/excel/unhide-the-first-column-or-row-in-a-worksheet
  - https://support.microsoft.com/en-us/excel/format-numbers
  - https://support.microsoft.com/en-us/excel/functions/subtotal-function
  - https://support.microsoft.com/en-us/excel/find-and-select-cells-that-meet-specific-conditions-in-excel
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rows and columns (Excel)

**Goal:** reshape a sheet without breaking formulas.

## Insert and delete
- Select a whole row (click the row number) or column (click the letter); `Shift+Space` selects the
  row, `Ctrl+Space` the column (the same keys work in Google Sheets).
- Insert: `Ctrl+Plus` (`Ctrl+Shift+Plus` opens the Insert dialog for cells). Delete: `Ctrl+Minus`.
- Changed your mind right after deleting? `Ctrl+Z` restores it.

## Width and height
- Drag the boundary to the right of a column heading. **Double-click** it to AutoFit to the contents;
  select several columns first to fit them all, or **Select All** and double-click any boundary to fit
  every column.
- Exact sizes: **Home › Cells › Format › Column Width** (or *AutoFit Column Width*, *Row Height*,
  *AutoFit Row Height*); or right-click the column › *Column Width*.
- `#####` in a number cell usually means the column is too narrow; widen it.

## Hide and unhide
- Select the rows or columns › right-click › **Hide**. A double line between headings shows something is
  hidden.
- Unhide: select the rows or columns on both sides › right-click › **Unhide**, or double-click the
  double line.
- Column A hidden? Right-click the column B header › **Unhide Columns**, or type `A1` in the Name Box and
  use **Home › Format › Hide & Unhide › Unhide Columns**. (Row 1 works the same way.)

## Gotchas
- Check what depends on a row before deleting it: Go To Special › **Dependents** selects the formulas
  that refer to the active cell.
- `SUM` includes rows you hid by hand; `=SUBTOTAL(109,...)` skips them. To copy without hidden rows, use
  Go To Special › **Visible cells only** first.
- Hidden data is not secret: anyone can unhide it. Remove sensitive columns before sharing.

## Verify
- [ ] No `#REF!` appears after the change; totals still add up.

## Checked
- 2026-10-27, against Microsoft Support (Excel for Microsoft 365) and Google Docs Editors Help as
  published on that date: row/column selection, insert/delete and undo shortcuts, AutoFit by
  double-click and Select All, Format › Column Width / AutoFit, `#####` meaning, hide/unhide and the
  double-line indicator, unhiding column A or row 1, SUBTOTAL 109, Go To Special Dependents and Visible
  cells only.

Method: documentation only; no commands were run.
