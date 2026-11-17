---
id: computing-software.general-digital-literacy.office-suites.filter-sort-unique-dynamic-arrays
name: filter-sort-unique-dynamic-arrays
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, formulas, functions, dynamic-arrays, filter-function, unique-function, sort-function]
level: advanced
status: docs-checked
description: "Use Excel 365 and Google Sheets dynamic array functions FILTER, SORT, SORTBY, UNIQUE and SEQUENCE, and fix #SPILL! errors."
sources:
  - https://support.microsoft.com/en-us/office/unique-function-c5ab87fd-30a3-4ce9-9d1a-40204fb85e1e
  - https://support.microsoft.com/en-us/excel/how-to-correct-a-spill-error
  - https://support.microsoft.com/en-us/excel/spilled-range-operator
  - https://support.microsoft.com/en-us/office/implicit-intersection-operator-ce3be07b-0101-4450-a24e-c1c999be2b34
  - https://support.microsoft.com/en-us/office/dynamic-array-formulas-and-spilled-array-behavior-205c6b06-03ba-4151-89a1-87a7eb36e531
  - https://support.google.com/docs/table/25273
  - https://github.com/LibreOffice/help/blob/master/source/text/scalc/01/func_unique.xhp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# FILTER, SORT, UNIQUE dynamic arrays

One formula returns many cells that *spill* into the range below/right. Available in Microsoft 365,
Excel 2021 and 2024 (Microsoft lists UNIQUE for those versions), Google Sheets and LibreOffice 24.8+.

## Core formulas
- `=UNIQUE(B2:B500)` distinct list; `=UNIQUE(B2:B500,,TRUE)` values appearing once only.
- `=SORT(A2:D500,3,-1)` sort by 3rd column descending.
- `=SORTBY(A2:A500,C2:C500,-1)` sort one range by another (Excel; not in the Google Sheets function
  list).
- `=FILTER(A2:D500,(C2:C500="North")*(D2:D500>1000),"None")`: `*` = AND, `+` = OR; third argument
  is shown when nothing matches.
- `=SORT(UNIQUE(FILTER(B2:B500,C2:C500="Open")))` combined.
- `=SEQUENCE(12)` numbers 1-12; `=COUNTA(UNIQUE(B2:B500))` count distinct.
- Refer to a whole spill with `#` (Excel): with `=SEQUENCE(10)` in A2, `=SUM(A2#)` totals the
  whole spilled range and follows it as it resizes.

## Google Sheets
FILTER, UNIQUE and SEQUENCE exist; `=QUERY(A1:D500,"select A,sum(D) where C='North' group by A")`
is a powerful extra.

## #SPILL! causes
- Something is in the way: clear the cells in the spill area (Excel's error menu offers *Select
  Obstructing Cells*).
- Inside an Excel Table: spilled array formulas are not supported in Tables; put the formula
  outside.
- Merged cells in the spill range.
- Whole-column references such as `VLOOKUP(A:A,...)` try to return about 1,048,576 results and run
  past the sheet edge; reference only the cells you need.

## Gotchas
- Excel versions without dynamic arrays cannot spill; legacy Ctrl+Shift+Enter array formulas
  return a fixed-size result.
- Excel adds `@` (implicit intersection) to older formulas that could return several cells;
  removing it lets a multi-cell result spill.

## Verify
- [ ] Add a new matching row in the source: the result updates without editing the formula (use a
  Table as source so the range grows).

## Checked

2026-10-27. Documentation checked against the current pages listed in sources. Microsoft UNIQUE page (Excel 365, 2024, 2021; exactly_once third argument; spills; resizes with a Table source), spill error pages (blocked range, tables, merged cells, whole-column references past the sheet edge), spilled range operator (SUM(A2#) example), implicit intersection (@ added to older formulas; removing it spills), dynamic array overview (not supported inside Tables; legacy Ctrl+Shift+Enter arrays are fixed size); Google Sheets function list (FILTER, UNIQUE, SEQUENCE, QUERY present; SORTBY absent); LibreOffice help sources (UNIQUE, SORT, FILTER from 24.8).
Method: documentation only; no commands were run.
