---
id: computing-software.general-digital-literacy.office-suites.format-as-table
name: format-as-table
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, spreadsheets, cell-formatting, excel-tables, format-as-table, banded-rows, total-row, structured-references, convert-to-range, sheets-tables]
level: intro
status: docs-checked
description: "Turn a data range into an Excel Table or Google Sheets table for banded rows, calculated columns, filter buttons and a total row."
sources:
  - https://support.microsoft.com/en-us/excel/overview-of-excel-tables
  - https://support.microsoft.com/en-us/excel/get-started/create-and-format-tables
  - https://support.microsoft.com/en-us/excel/get-started/total-the-data-in-an-excel-table
  - https://support.microsoft.com/en-us/excel/get-started/merge-and-unmerge-cells-in-excel
  - https://support.microsoft.com/en-us/accessibility/excel/keyboard-shortcuts-in-excel
  - https://support.google.com/docs/answer/14239833?hl=en
  - https://support.google.com/docs/answer/181110?hl=en
  - https://help.libreoffice.org/latest/en-US/text/scalc/00/00000412.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Format as Table

**Goal:** make a list of records behave as one unit that filters and totals itself.

## Excel
1. Click inside the data (one header row, no blank rows/columns) › **Home › Format as Table** › pick a
   style › confirm the range and tick **My table has headers**. `Ctrl+T` (or `Ctrl+L`) opens the Create
   Table dialog directly.
2. Table options include **Banded rows** and **Total Row** (on the table's Design tab). Each total cell
   has a drop-down (Sum, Average...) that writes a `SUBTOTAL` formula such as `=SUBTOTAL(109,[Midwest])`.
3. A formula typed in one cell of a table column becomes a **calculated column**, applied to every cell
   in that column.
4. Formulas can use **structured references** to table and column names instead of `A1` addresses.
5. Drag the sizing handle at the table's lower-right corner to resize it.

## Google Sheets
Select the range › **Format › Convert to table** (`Ctrl+Alt+T`): set a column type for each column
(placeholder chips help data entry), filter views and group-by views, and table formatting such as
alternating colours.

## LibreOffice Calc
No table object of the same kind; **Data › Define Range** gives the block a name as a database range.

## Gotchas
- **Merge & Center** is disabled inside an Excel table; keep headers in single cells.
- Structured references look strange to people used to `A1`; they are more robust, keep them.

## Verify
- [ ] Add a value to a calculated column's source: the formula result appears in every row, and the
  total row updates.

## Checked
- 2026-10-27, against Microsoft Support (Excel for Microsoft 365), Google Docs Editors Help and
  LibreOffice help (master) as published on that date: Format as Table and My table has headers,
  Ctrl+T/Ctrl+L, banded rows, Total Row drop-down and SUBTOTAL(109,...), calculated columns, structured
  references, sizing handle, Merge & Center disabled in tables, Sheets Convert to table and Ctrl+Alt+T,
  column types and views, Calc Data › Define Range.

Method: documentation only; no commands were run.
