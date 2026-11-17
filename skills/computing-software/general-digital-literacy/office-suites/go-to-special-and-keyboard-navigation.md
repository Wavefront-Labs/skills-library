---
id: computing-software.general-digital-literacy.office-suites.go-to-special-and-keyboard-navigation
name: go-to-special-and-keyboard-navigation
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, spreadsheets, worksheets, go-to-special, keyboard-navigation, select-blanks, visible-cells-only]
level: practitioner
status: docs-checked
description: "Move and select across big sheets with Ctrl+arrow keys, the Name Box and Go To Special to find blanks, formulas, constants or visible cells only."
sources:
  - https://support.microsoft.com/en-us/accessibility/excel/keyboard-shortcuts-in-excel
  - https://support.microsoft.com/en-us/excel/find-and-select-cells-that-meet-specific-conditions-in-excel
  - https://support.microsoft.com/en-us/excel/copy-visible-cells-only
  - https://support.microsoft.com/en-us/excel/unhide-the-first-column-or-row-in-a-worksheet
  - https://support.google.com/docs/answer/181110?hl=en
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Keyboard navigation and Go To Special

## Move fast in Excel (Windows)
| Keys | Does |
|---|---|
| Ctrl+Arrow | Jump to the edge of the current data region |
| Ctrl+Shift+Arrow | Extend the selection to the last non-blank cell |
| Ctrl+Home / Ctrl+End | Start of the sheet / last used cell (lowest used row of the rightmost used column) |
| Ctrl+Space / Shift+Space | Select column / row |
| Ctrl+A (inside data) | Select the current region (press again for the whole sheet) |
| Ctrl+PgUp / Ctrl+PgDn | Previous / next sheet |
| F5 or Ctrl+G | Go To |
Name Box (left of the formula bar): type a reference such as `A1` and press Enter to jump there.

## Google Sheets
Ctrl+Space / Shift+Space select column / row, Ctrl+A selects all, Ctrl+Home / Ctrl+End go to the start /
end of the sheet, and **Alt+Down / Alt+Up** move to the next / previous sheet (Option on Mac). Sheets has
no Go To Special dialog; use filters (filter by condition) to work on blanks.

## Go To Special (Excel: Home › Find & Select › Go To › Special, or Ctrl+G › Special)
Select one cell to search the whole sheet, or a range to search only that range.
- **Blanks**: select empty cells, type `=A2` (the cell above) and press **Ctrl+Enter** to fill every
  selected cell at once.
- **Constants / Formulas** (check boxes narrow the type): find hard-typed values that should be
  formulas, or select every formula cell.
- **Visible cells only**: only cells visible in a range that crosses hidden rows or columns; copy after
  this to leave hidden rows out. Not available in Excel for the web (there, only a filtered *table*
  copies visible cells only).
- Also: **Last cell**, **Row differences / Column differences**, **Precedents / Dependents**,
  **Conditional formats** and **Data validation** (All or Same).

## Gotchas
- Ctrl+End and Go To Special › Last cell count formatting as well as data, so they can land far below
  the real data.
- Ctrl+Enter fills every selected cell; leave the selection in place until done.

## Verify
- [ ] After filling blanks, Go To Special › Blanks no longer finds any in the range.

## Checked
- 2026-10-27, against Microsoft Support (Excel for Microsoft 365) and Google Docs Editors Help as
  published on that date: Excel navigation and selection shortcuts, Name Box navigation, Go To Special
  location and every option listed, visible-cells copying on the web, Ctrl+Enter fill; Sheets selection,
  navigation and sheet-switching shortcuts.

Method: documentation only; no commands were run.
