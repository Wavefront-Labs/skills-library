---
id: computing-software.general-digital-literacy.office-suites.if-function-and-logical-tests
name: if-function-and-logical-tests
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, spreadsheets, functions, if-function, logical-tests, and-or, ifs, iferror, nested-if, comparison-operators]
level: intro
status: docs-checked
description: "Use IF with comparison operators, AND/OR, IFS and IFERROR to make spreadsheet cells show different results based on conditions in Excel, Sheets and Calc."
sources:
  - https://support.microsoft.com/en-us/office/ifs-function-36329a26-37b2-467c-972b-4a39bd951d45
  - https://support.google.com/docs/table/25273
  - https://github.com/LibreOffice/help/blob/master/source/text/scalc/01/func_ifs.xhp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# IF and logical tests

**Goal:** a cell that decides: "Paid"/"Due", pass/fail, bonus or none.

## Shape
`=IF(test, value_if_true, value_if_false)`
- Tests use `=  <>  >  <  >=  <=`.
- Text results go in quotes: `=IF(C2>=50,"Pass","Fail")`.
- Numbers or formulas: `=IF(B2>1000,B2*0.05,0)` (5% bonus over 1000).
- Blank check: `=IF(D2="","Not paid","Paid")`.

## Several conditions
- Both true: `=IF(AND(B2>=18,C2="Yes"),"Eligible","No")`
- Either true: `=IF(OR(B2="VIP",C2>500),"Free delivery","Standard")`
- Bands without deep nesting: `=IFS(C2>=70,"A",C2>=60,"B",C2>=50,"C",TRUE,"Fail")` (Excel 2019 and
  later, Google Sheets, LibreOffice Calc 5.2+). Order matters: highest threshold first.

## Hide errors you expect
`=IFERROR(B2/C2,0)` shows 0 instead of `#DIV/0!`. Use sparingly: it hides real mistakes too.

## Gotchas
- `"50"` in quotes is text; `C2>="50"` compares text and gives odd results. No quotes round numbers.
- Every opening bracket needs a closing one.
- A cell that looks empty but has a space isn't `""`. Use `TRIM()` on imported data.

## Verify
- [ ] Test each branch with a value just above, at and below each threshold.

## Checked

2026-10-27. Documentation checked against the current pages listed in sources. Microsoft IFS page (Excel 2019, 2021, 2024, Microsoft 365; up to 127 conditions), Google Sheets function list (IFS present), LibreOffice help source func_ifs.xhp (available from 5.2).
Method: documentation only; no commands were run.
