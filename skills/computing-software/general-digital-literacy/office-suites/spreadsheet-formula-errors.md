---
id: computing-software.general-digital-literacy.office-suites.spreadsheet-formula-errors
name: spreadsheet-formula-errors
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, spreadsheets, formulas, formula-errors, div-0, ref-error, value-error, name-error, circular-reference, trace-precedents]
level: intro
status: docs-checked
description: "Read and fix spreadsheet error values (#DIV/0!, #N/A, #REF!, #VALUE!, #NAME?, ####, circular references) in Excel, Google Sheets and LibreOffice Calc."
sources:
  - https://support.microsoft.com/en-us/excel/detect-formula-errors-in-excel
  - https://support.microsoft.com/en-us/excel/remove-or-allow-a-circular-reference-in-excel
  - https://support.microsoft.com/en-us/excel/how-to-correct-a-spill-error
  - https://support.microsoft.com/en-us/office/how-to-correct-a-error-bf801d0a-2a6e-44bd-a70e-0f780ae8f11e
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Spreadsheet formula errors

**Goal:** recognise what each error means and fix the cause.

| Shows | Means | Usual fix |
|---|---|---|
| `#DIV/0!` | divided by zero or by an empty cell | fill the divisor or `=IF(C2=0,"",B2/C2)` |
| `#N/A` | a value is not available, often a lookup that found nothing | check spelling, spaces, number-vs-text |
| `#REF!` | a cell reference is not valid, often a deleted cell | undo the deletion or rewrite the reference |
| `#VALUE!` | data types that don't mix, e.g. text in maths | clean the input, `VALUE()` |
| `#NAME?` | Excel does not recognise text in the formula (misspelt function or name) | fix the spelling; put text in quotes |
| `#NUM!` | invalid numeric value | check inputs (e.g. negative square root) |
| `#SPILL!` (Excel) | dynamic result blocked | clear cells in the way |
| `#####` | not a formula error: column too narrow, or a negative date or time | widen the column or fix the formula |

LibreOffice Calc has its own error codes; see its help for the list.

## Find the source
- Excel marks errors with a triangle in the top-left corner of the cell; Formulas › Formula Auditing ›
  **Error Checking** steps through them one at a time.
- **Evaluate Formula** (Excel on Windows) shows a nested formula's intermediate results in
  calculation order, one cell at a time.

## Circular reference
A formula that refers to its own cell (directly or round a chain). Excel warns the first time it
finds one and shows "Circular References" in the status bar, with a cell address when the cell is
on the current sheet. Fix the formula rather than turning on iterative calculation (File › Options
› Formulas), which is off by default.

## Gotchas
- Wrapping everything in `IFERROR` hides real problems; fix first, suppress only expected cases.
- An error in one cell spreads to every total that depends on it; fix the first one in the chain.

## Verify
- [ ] Error Checking reports no errors (or only ones you chose to allow).

## Checked

2026-10-27. Documentation checked against the current pages listed in sources. Microsoft Detect formula errors page (meaning of #DIV/0!, #N/A, #REF!, #VALUE!, #NAME?, #NUM!; Error Checking and Evaluate Formula), circular reference page (warning on first occurrence, Circular References in the status bar, iterative calculation off by default), #SPILL! pages and the ##### page (narrow column or negative date or time).
Method: documentation only; no commands were run.
