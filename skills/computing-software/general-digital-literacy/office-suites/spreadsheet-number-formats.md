---
id: computing-software.general-digital-literacy.office-suites.spreadsheet-number-formats
name: spreadsheet-number-formats
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, spreadsheets, cell-formatting, number-formats, currency-format, percentage-format, date-format, custom-number-format, leading-zeros]
level: intro
status: docs-checked
description: "Format cells as currency, percentage, dates, thousands separators or text, write custom number formats and keep leading zeros in Excel, Sheets and Calc."
sources:
  - https://support.microsoft.com/en-us/excel/format-numbers
  - https://support.microsoft.com/en-us/excel/review-guidelines-for-customizing-a-number-format
  - https://support.microsoft.com/en-us/excel/keeping-leading-zeros-and-large-numbers
  - https://support.microsoft.com/en-us/accessibility/excel/keyboard-shortcuts-in-excel
  - https://support.google.com/docs/answer/46973?hl=en
  - https://support.google.com/docs/answer/181110?hl=en
  - https://help.libreoffice.org/latest/en-US/text/scalc/00/00000405.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Number, currency, percentage and date formats

**Goal:** numbers that read correctly without changing their stored value.

## Quick formats
- **Excel:** `Ctrl+1` (`Cmd+1` on Mac) opens Format Cells › *Number* tab for every format.
  `Ctrl+Shift+%` applies Percentage with no decimals.
- **Google Sheets:** **Format › Number** › pick a format, or *Custom number format* / *Custom date and
  time* at the bottom. Shortcuts: `Ctrl+Shift+4` currency, `Ctrl+Shift+5` percentage.
- **Calc:** **Format › Cells** (`Ctrl+1`).

## Custom formats (Excel; Sheets and Calc use similar codes)
| Code | Shows 1234.5 as | Why |
|---|---|---|
| `#,##0.00` | 1,234.50 | comma between `#`/`0` = thousands separator |
| `0.0%` | 123450.0% | `%` multiplies by 100 (store 0.12 for 12%) |
| `00000` | 01235 | `0` shows padding zeros: fixed-length codes |
| `#,##0,"k"` | 1k | a comma after the last digit placeholder scales by 1,000 |
| `dd mmm yyyy` | (a date) 05 Jan 2026 | `dd` day with zero, `mmm` Jan-Dec, `yyyy` four-digit year |
Custom formats are saved with the workbook.

## Leading zeros and IDs
Phone numbers, account numbers and codes are text, not numbers: set the column to **Text** (`Ctrl+1` ›
Number › Text) before typing or pasting. Excel otherwise removes leading zeros and keeps only 15 digits of
long numbers (card numbers, IDs), showing them in scientific notation.

## Gotchas
- Formatting doesn't round the stored value; totals can differ by a penny from displayed numbers.
- `#####` usually means the column is too narrow for the formatted number; widen it.
- Regional settings decide separators and default currency; check on the recipient's side.

## Verify
- [ ] Formula bar shows the true value; cell shows the intended format.

## Checked
- 2026-10-27, against Microsoft Support (Excel for Microsoft 365), Google Docs Editors Help and
  LibreOffice help (master) as published on that date: Ctrl+1/Cmd+1 and the Text category,
  Ctrl+Shift+%, Sheets Format › Number with custom options and Ctrl+Shift+4/5, Calc Format › Cells,
  custom codes (`0`, `#`, thousands comma and scaling, `%`, `dd`/`mmm`/`yyyy`), formats saved with the
  workbook, leading-zero and 15-digit behaviour, `#####` meaning.

Method: documentation only; no commands were run.
