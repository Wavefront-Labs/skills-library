---
id: computing-software.general-digital-literacy.office-suites.subtotals-and-outline
name: subtotals-and-outline
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, sort-and-filter, subtotals, outline-groups, subtotal-function, aggregate, group-rows]
level: practitioner
status: docs-checked
description: "Insert automatic subtotals by group with Excel's Subtotal command, collapse levels with the outline, and use SUBTOTAL and AGGREGATE that ignore hidden rows."
sources:
  - https://support.microsoft.com/en-us/excel/insert-subtotals-in-a-list-of-data-in-a-worksheet
  - https://support.microsoft.com/en-us/excel/functions/subtotal-function
  - https://support.microsoft.com/en-us/office/aggregate-function-43b9278e-6aa7-4f17-92b6-e19993fa26df
  - https://github.com/LibreOffice/help/blob/master/source/text/scalc/guide/subtotaltool.xhp
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# Subtotals and outline summaries

## Subtotal command (Excel)
1. **Sort** by the grouping column first (e.g. Region).
2. Click in the data › **Data › Outline › Subtotal** › *At each change in* Region › *Use function*
   Sum › *Add subtotal to* Sales (and others) › OK.
3. The outline symbols at the left show only the subtotals and grand totals; the plus and minus
   symbols show or hide detail rows.
4. Remove: Data › Outline › Subtotal › **Remove All**.
- The Subtotal command is unavailable on an Excel Table (convert it to a range, or use a
  PivotTable instead).

## SUBTOTAL function
`=SUBTOTAL(9,C2:C500)` sums only the rows left visible by a filter. 9 is SUM and 1 is AVERAGE;
codes 101-111 are the same functions but also leave out rows you hid manually. Table total rows
use SUBTOTAL by default.

## AGGREGATE (Excel)
`=AGGREGATE(9,6,C2:C500)` sums while ignoring error values (option 6). Option 5 ignores hidden
rows and option 7 ignores both hidden rows and error values.

## Google Sheets
Use `=SUBTOTAL(9,C2:C500)`, a pivot table (Insert › Pivot table), or
`=QUERY(A1:C500,"select A, sum(C) group by A")`.

## LibreOffice Calc
Data › Subtotals opens the Subtotals dialog.

## Gotchas
- Unsorted data gives a subtotal at every change, i.e. many tiny groups.
- Grand totals made with SUM will double-count subtotal rows already in the range.

## Verify
- [ ] Grand total equals SUM of the raw column taken before inserting subtotals.

## Checked

2026-10-27. Documentation checked against the current pages listed in sources. Microsoft Insert subtotals page (sort first, Data, Outline, Subtotal, At each change in, Use function, Add subtotal to, Remove All, not supported in Tables), SUBTOTAL page (101-111 also leave out manually hidden rows, 9 is SUM, 101 is AVERAGE; Table total rows use SUBTOTAL), AGGREGATE page (options 0-7: 5 hidden rows, 6 error values, 7 both), LibreOffice help source subtotaltool.xhp (Data, Subtotals).
Method: documentation only; no commands were run.
