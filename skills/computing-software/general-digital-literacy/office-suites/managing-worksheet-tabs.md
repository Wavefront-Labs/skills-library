---
id: computing-software.general-digital-literacy.office-suites.managing-worksheet-tabs
name: managing-worksheet-tabs
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, spreadsheets, worksheets, worksheet-tabs, rename-sheet, move-or-copy-sheet, tab-colour, hide-sheet, 3d-reference]
level: intro
status: docs-checked
description: "Add, rename, colour, reorder, copy, hide and reference worksheets (sheet tabs) in Excel, Google Sheets and LibreOffice Calc."
sources:
  - https://support.microsoft.com/en-us/excel/get-started/insert-or-delete-a-worksheet
  - https://support.microsoft.com/en-us/excel/rename-a-worksheet
  - https://support.microsoft.com/en-us/excel/add-a-background-color-to-a-sheet-tab
  - https://support.microsoft.com/en-us/excel/get-started/move-or-copy-worksheets-or-worksheet-data
  - https://support.microsoft.com/en-us/excel/hide-or-unhide-worksheets
  - https://support.microsoft.com/en-us/accessibility/excel/keyboard-shortcuts-in-excel
  - https://support.google.com/docs/answer/181110?hl=en
  - https://help.libreoffice.org/latest/en-US/text/scalc/guide/cellreferences.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managing worksheet tabs

**Goal:** organise a workbook into well-named sheets.

## Basics (Excel)
- Add: the **New Sheet** plus icon next to the tabs, **Home › Insert › Insert Sheet**, or `Shift+F11`
  (also inserts a sheet in Google Sheets).
- Rename: double-click the tab, or right-click › **Rename**, or `Alt+H, O, R`. Names can't be blank or
  longer than 31 characters, can't contain `/ \ ? * : [ ]`, can't begin or end with an apostrophe, and
  can't be "History".
- Colour: right-click › **Tab Color** › pick a colour (*No Color* removes it). Tab font can't be changed.
- Move: drag the tab. Switch: `Ctrl+PgDn` / `Ctrl+PgUp`. Google Sheets: `Alt+Down` / `Alt+Up`
  (`Option` on Mac).
- Delete: right-click the tab › **Delete**.

## Copy a sheet (Excel)
Right-click the tab › **Move or Copy** › tick **Create a copy** › choose *Before sheet* (and *To book* for
another open workbook) › OK. Or hold `Ctrl` and drag the tab (`Option` on Mac).

## Hide
Excel: right-click › **Hide**; right-click any visible tab › **Unhide** › pick the sheets › OK. Data on a
hidden sheet can still be referenced from other sheets, so hiding is tidiness, not security.

## Refer to another sheet
LibreOffice Calc separates sheet and cell with a dot: `=Sheet2.A1`.

## Gotchas
- Save before deleting sheets you might need back.

## Verify
- [ ] Each tab has a meaningful name; cross-sheet formulas show values, not `#REF!`.

## Checked
- 2026-10-27, against Microsoft Support (Excel for Microsoft 365), Google Docs Editors Help and
  LibreOffice help (master) as published on that date: insert/delete sheet, Shift+F11 in Excel and
  Sheets, rename methods and name rules, Tab Color, Move or Copy with Create a copy, Ctrl/Option-drag
  copy, hide/unhide and referencing hidden sheets, sheet-switch shortcuts, Calc dot reference syntax.

Method: documentation only; no commands were run.
