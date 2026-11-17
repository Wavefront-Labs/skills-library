---
id: computing-software.general-digital-literacy.office-suites.named-ranges
name: named-ranges
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, spreadsheets, worksheets, named-ranges, name-manager, defined-names]
level: practitioner
status: docs-checked
description: "Name cells and ranges in Excel and Google Sheets so formulas read =SUM(Sales), jump to ranges by name, and fix #NAME? and broken names in Name Manager."
sources:
  - https://support.microsoft.com/en-us/excel/names-in-formulas
  - https://support.microsoft.com/en-us/office/rename-a-cell-or-range-names-in-formulas-define-and-use-names-in-formulas-4d0f13ac-53b7-422e-afd2-abd7ff379c64
  - https://support.microsoft.com/en-us/accessibility/excel/keyboard-shortcuts-in-excel
  - https://support.google.com/docs/answer/63175
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Named ranges

**Why:** `=Price*VAT_Rate` beats `=B2*$H$1`; names are readable and reusable.

## Create
- Excel: select the range, type the name in the **Name Box** (left of the formula bar), press Enter.
- **Formulas › Create from Selection**: names cells from the labels in the top row, left column,
  bottom row or right column of the selection.
- Sheets: select the cells, then **Data › Named ranges** and enter the name.
- Excel rules: the first character is a letter, underscore or backslash; no spaces (use
  `Tax_Rate`); not a cell reference such as `Z$100` or `R1C1`; up to 255 characters.
- Sheets rules: letters, numbers and underscores only; cannot start with a number or the words
  true/false; not in A1 or R1C1 form; 1-250 characters.

## Use
- In formulas: type the name instead of the range. **F3** (Excel on Windows) opens the Paste Name
  box when names exist in the workbook.
- Navigate: **F5** (Go To) in Excel on Windows.

## Manage
**Formulas › Name Manager**: create, edit and delete names; the *Refers to* column shows and edits
what each name points at; the *Names With Errors* filter shows names whose values are errors such
as `#REF!`, `#VALUE!` or `#NAME?`.

## Verify
- [ ] Name Manager shows no names with errors and each name's range is the one you intended.

## Checked

2026-10-27. Documentation checked against the current pages listed in sources. Microsoft names-in-formulas page (first character letter, underscore or backslash; no spaces; not a cell reference such as Z$100 or R1C1; up to 255 characters; Name Manager Refers to and Names With Errors filter), the define-names page (Name Box, Create from Selection, Name Manager), keyboard shortcuts (F3 pastes a name, F5 opens Go To; no Name Manager shortcut listed), Google Sheets named ranges help (Data, Named ranges; naming rules).
Method: documentation only; no commands were run.
