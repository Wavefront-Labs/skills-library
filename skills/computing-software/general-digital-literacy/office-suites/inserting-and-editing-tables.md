---
id: computing-software.general-digital-literacy.office-suites.inserting-and-editing-tables
name: inserting-and-editing-tables
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, word-processing, word-tables, insert-table, document-tables, table-rows, autofit, header-row, convert-text-to-table]
level: intro
status: docs-checked
description: "Insert a table, add or delete rows and columns, AutoFit widths, repeat header rows and convert text to a table in Word, Google Docs and LibreOffice."
sources:
  - https://support.microsoft.com/en-us/word/convert-text-to-a-table-or-a-table-to-text
  - https://support.microsoft.com/en-us/word/resize-a-table-column-or-row
  - https://support.microsoft.com/en-us/word/repeat-table-header-on-subsequent-pages
  - https://support.microsoft.com/en-us/office/keyboard-shortcuts-in-word-95ef89dd-7142-4b50-afb2-f762f663ceb2
  - https://support.google.com/docs/answer/1696711
  - https://help.libreoffice.org/latest/en-US/text/swriter/04/01020000.html
  - https://help.libreoffice.org/latest/en-US/text/swriter/01/05090300.html
  - https://help.libreoffice.org/latest/en-US/text/swriter/00/00000406.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inserting and editing tables in documents

**Goal:** lay out tabular information with a real table, not tabs and spaces.

## Insert
- **Word:** Insert › Table.
- **Google Docs:** Insert › Table › choose rows and columns (up to 20 x 20 cells).
- **LibreOffice:** `Ctrl+F12` or Table › Insert Table.
- Word: `Tab` moves to the next cell, `Shift+Tab` back; `Tab` at the end of the last row adds a row.

## Rows and columns
- Google Docs: right-click a cell › Insert row above/below, Insert column left/right; Delete row,
  Delete column or Delete table.
- Word and LibreOffice: use the table's right-click menu or the table tabs/menus to insert and delete
  rows and columns.

## Widths
- Word: Table Layout › **AutoFit** › AutoFit Contents (tight) or AutoFit Window (full width);
  **Distribute Columns** evens them out.
- Docs: right-click › Distribute columns; or Format › Table › Table options › Column width.

## Long tables
Word: select the first row › Table Layout › **Repeat Header Rows** so it shows on every page.
Docs: Format › Table › Table options › *Pin header row(s)*. LibreOffice: Table Properties › Text Flow ›
*Repeat heading*.

## Text to table
Word: separate columns with tabs or commas and rows with paragraph marks › select › Insert › Table ›
**Convert Text to Table**. LibreOffice: Table › Convert › Text to Table.

## Gotchas
- Tables used purely for page layout confuse screen readers; use them for data.
- Sorting rows: Google Docs right-click › Sort table (pinned header rows are not sorted).

## Verify
- [ ] Header row repeats on page 2 in print preview.

## Checked
2026-10-27 against Microsoft Support Word table pages and keyboard shortcuts (Microsoft 365), Google Docs
Editors Help (Add and edit tables) and the LibreOffice help (master). Confirmed: Docs 20 x 20 limit,
row/column menu items, Distribute columns, Table options and Pin header rows, Sort table; Word Tab
navigation, AutoFit, Distribute Columns, Repeat Header Rows and Convert Text to Table; LibreOffice
Ctrl+F12, Repeat heading and Table › Convert › Text to Table. Removed unconfirmed grid sizes, hover-insert,
Delete/Backspace and Word sort claims. Method: documentation only; no commands were run.
