---
id: computing-software.general-digital-literacy.office-suites.paste-special-values-and-transpose
name: paste-special-values-and-transpose
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, spreadsheets, worksheets, paste-special, paste-values, transpose]
level: practitioner
status: docs-checked
description: "Use Paste Special in Excel and Google Sheets to paste values only, formats, column widths, transposed data, or do maths on a range while pasting."
sources:
  - https://support.microsoft.com/en-us/excel/paste-options
  - https://support.microsoft.com/en-us/accessibility/excel/keyboard-shortcuts-in-excel
  - https://support.microsoft.com/en-us/office/copy-and-paste-specific-cell-content-in-excel-for-mac-a956b1c3-cd5a-4245-852c-42e8f83ffe71
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Paste Special: values, formats, transpose

## Excel
Copy (Ctrl+C), select the destination, then **Ctrl+Alt+V** (or Home › Paste › Paste Special):
- **Values**: freezes formula results as numbers/text. Use before sending a sheet or deleting the
  source columns.
- **Formatting**: copy the look only.
- **Keep Source Column Widths**: match widths of the copied columns.
- **Formulas**: formulas without the source formatting.
- **Transpose**: rows become columns (a checkbox in the dialog and a command on the Paste menu).
- **Operation: Multiply / Add**: e.g. type 1.1 in a cell, copy it, select prices, Paste Special ›
  Values + Multiply = 10% increase in place. The dialog offers None, Add, Subtract, Multiply and
  Divide.
- **Skip blanks**: blank source cells do not overwrite destination values.

## Gotchas
- Some Paste Special options are greyed out depending on what was copied.

## Verify
- [ ] Click a pasted cell: the formula bar shows a value, not `=...`, when you meant values.

## Checked

2026-10-27. Documentation checked against the current pages listed in sources. Microsoft Paste options page (Ctrl+Alt+V opens Paste Special; Windows ribbon options Keep Source Column Widths, Transpose, Formulas, Values, Formatting; some Paste Special options are greyed out depending on what was copied), Paste Special dialog operations (None, Add, Subtract, Multiply, Divide) and Skip blanks and Transpose checkboxes.
Method: documentation only; no commands were run.
