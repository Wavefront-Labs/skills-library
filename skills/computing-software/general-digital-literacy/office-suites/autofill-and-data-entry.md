---
id: computing-software.general-digital-literacy.office-suites.autofill-and-data-entry
name: autofill-and-data-entry
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, spreadsheets, worksheets, autofill-series, fill-handle, flash-fill, data-entry, fill-down, smart-fill]
level: intro
status: docs-checked
description: "Enter spreadsheet data quickly with the fill handle, AutoFill series, Fill Down/Right, Ctrl+Enter and Flash Fill / Smart Fill in Excel, Sheets and Calc."
sources:
  - https://support.microsoft.com/en-us/excel/get-started/fill-data-automatically-in-worksheet-cells
  - https://support.microsoft.com/en-us/excel/using-flash-fill-in-excel
  - https://support.microsoft.com/en-us/accessibility/excel/keyboard-shortcuts-in-excel
  - https://support.microsoft.com/en-us/excel/format-numbers
  - https://support.google.com/docs/answer/181110?hl=en
  - https://support.google.com/docs/answer/9914525?hl=en
  - https://help.libreoffice.org/latest/en-US/text/scalc/04/01020000.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AutoFill and fast data entry

**Goal:** fill series and repeat values without typing each cell.

## Fill handle (Excel)
Select the starting cell(s) and drag the fill handle (the small square at the bottom-right of the selection).
| Start with | Drag gives |
|---|---|
| `1` and `2` in two cells (both selected) | 3, 4, 5... (the step is learnt) |
| `2` and `4` | 6, 8... |
| `2` in one cell only | 2, 2, 2... |
After dragging, the **Auto Fill Options** button offers other fill choices.

## Keyboard
- `Ctrl+D` fill down, `Ctrl+R` fill right (Excel and Google Sheets).
- `Ctrl+Enter` fills the selected range with the current entry (Excel; "Fill range" in Sheets).
- LibreOffice Calc: `Alt+Enter` (Option+Enter on macOS) fills the selected range with the formula typed on the Input line.

## Pattern filling
- **Excel Flash Fill**: type the result you want for the first row (for example a full name built from
  first and last name columns), then press `Ctrl+E` or choose **Data › Flash Fill**. If no preview
  appears automatically, the *Automatically Flash Fill* option may be off.
- **Google Sheets Smart Fill** suggests completions once it detects a pattern; trigger it with
  `Ctrl+Shift+Y` (`Cmd+Shift+Y` on Mac). Click a filled cell to see the formula it used.

## Gotchas
- Leading zeros (phone numbers, postal codes) are removed when Excel converts the entry to a number;
  format the column as **Text** first (`Ctrl+1` › Number › Text).
- Check the end of a long series, not just the start.

## Verify
- [ ] Last filled cell holds the value you expected.

## Checked
- 2026-10-27, against Microsoft Support (Excel for Microsoft 365), Google Docs Editors Help and
  LibreOffice Calc help (latest) as published on that date: fill-handle series rules, Auto Fill Options,
  Ctrl+D/Ctrl+R/Ctrl+Enter in Excel and Sheets, Flash Fill (Ctrl+E, Data › Flash Fill), Smart Fill
  shortcut, Calc Alt+Enter fill, Text format for leading zeros.

Method: documentation only; no commands were run.
