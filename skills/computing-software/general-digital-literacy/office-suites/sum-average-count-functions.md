---
id: computing-software.general-digital-literacy.office-suites.sum-average-count-functions
name: sum-average-count-functions
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, spreadsheets, functions, sum-function, autosum, average, count, counta, min-max, sumif, countif]
level: intro
status: docs-checked
description: "Use SUM, AVERAGE, MIN, MAX, COUNT, COUNTA and AutoSum, plus SUMIF/COUNTIF for conditional totals, in Excel, Google Sheets and LibreOffice Calc."
sources:
  - https://support.microsoft.com/en-us/accessibility/excel/keyboard-shortcuts-in-excel
  - https://support.microsoft.com/en-us/excel/functions/average-function
  - https://support.microsoft.com/en-us/office/sumifs-function-c9e748f5-7ea7-455d-9406-611cebce642b
  - https://support.microsoft.com/en-us/office/counta-function-7dc98875-d5c1-46f1-9a82-53f3219e2509
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SUM, AVERAGE, COUNT and friends

**Goal:** summarise a column correctly.

## AutoSum
Select the cell under a column of numbers, then `Alt+=` (Excel on Windows; Mac `Shift+Cmd+T`) or
Home › AutoSum. Check the highlighted range before pressing Enter.

## The core functions
| Function | Returns | Note |
|---|---|---|
| `=SUM(B2:B50)` | total | ranges with `:`; several ranges with `,` |
| `=AVERAGE(B2:B50)` | mean | skips text and empty cells in the range, counts zeros |
| `=MIN()` / `=MAX()` | smallest / largest | |
| `=COUNT(B2:B50)` | how many **numbers** | skips text, logicals and errors |
| `=COUNTA(A2:A50)` | how many **non-empty** cells | counts any content, including errors and empty text |
| `=SUMIF(A2:A50,"Food",B2:B50)` | total where A = Food | |
| `=COUNTIF(B2:B50,">100")` | how many over 100 | |
| `=SUMIFS(C:C,A:A,"Food",B:B,"2026")` | total with several conditions | sum range comes first |

## Gotchas
- LibreOffice Calc help writes arguments separated by `;`, for example
  `=SUMIF(A2:A50;"Food";B2:B50)`; use whichever separator your app accepts.
- Check the range an AutoSum picked: a gap in the data can leave part of it out.

## Verify
- [ ] Add up three or four rows by hand and compare with the formula.

## Checked

2026-10-27. Documentation checked against the current pages listed in sources. Microsoft keyboard shortcuts (Alt+= on Windows and Shift+Cmd+T on Mac insert the sum), AVERAGE (skips text, logicals and empty cells in a reference, counts zeros), SUMIFS (argument order sum_range, then criteria pairs), COUNTA and COUNT definitions, LibreOffice help examples (semicolon-separated arguments).
Method: documentation only; no commands were run.
