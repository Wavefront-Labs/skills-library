---
id: computing-software.general-digital-literacy.office-suites.data-validation-and-drop-down-lists
name: data-validation-and-drop-down-lists
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, spreadsheets, sort-and-filter, data-validation, drop-down-list, input-message, error-alert, dependent-dropdown, checkboxes]
level: intro
status: docs-checked
description: "Restrict what can be typed in cells with data validation, add drop-down lists, input messages and error alerts in Excel, Google Sheets and LibreOffice Calc."
sources:
  - https://support.microsoft.com/en-us/office/apply-data-validation-to-cells-29fecbcc-d1b9-42c1-9d76-eff3ce5f7249
  - https://support.microsoft.com/en-us/excel/display-or-hide-circles-around-invalid-data
  - https://support.microsoft.com/en-us/excel/using-check-boxes-in-excel
  - https://support.google.com/docs/answer/186103
  - https://github.com/LibreOffice/help/blob/master/source/text/scalc/guide/validity.xhp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Data validation and drop-down lists

**Goal:** stop bad entries (typos, wrong dates, impossible numbers) at the point of typing.

## Drop-down list
- **Excel:** select cells › Data › **Data Validation** › Settings › Allow: *List* › Source: type
  `Yes,No,Maybe` or choose a range such as `=$H$2:$H$10`. Keep *In-cell dropdown* ticked.
- **Google Sheets:** Insert › **Dropdown**, or Data › Data validation › Add rule. Advanced options
  set the display style (Chip, Arrow or Plain text).
- **Calc:** Data › Validity › Allow: List.

## Messages
- **Input message** (Excel) / **Input Help** (Calc): a tooltip when the cell is selected ("Enter
  date as dd/mm/yyyy").
- **Error alert:** Excel *Stop* blocks the entry and *Warning* lets the user continue (a third,
  informational style is also offered); Calc offers Stop, Warning and Information.
- Sheets: off-list entries are rejected by default; Advanced options › *Show a warning* allows them.

## Checkboxes
Excel (desktop, not Excel for the web): select the cells, then Insert › **Checkbox**.

## Gotchas
- Validation guards typing; values pasted or filled in, or produced by formulas, can still be
  invalid. In Excel, Data › Data Validation arrow › **Circle Invalid Data** marks them (and *Clear
  Validation Circles* removes the circles).

## Verify
- [ ] Type a wrong value: you get your error alert; Circle Invalid Data finds nothing.

## Checked

2026-10-27. Documentation checked against the current pages listed in sources. Microsoft Apply data validation page (Data, Data Validation, Allow List, In-cell dropdown, Input message tab, Stop and Warning styles), Display or hide circles around invalid data (circles also mark pasted, filled and formula values), checkbox page (Insert, Checkbox; not in Excel for the web), Google Sheets dropdown help (Insert, Dropdown; invalid entries rejected by default, Show a warning in Advanced options; Chip, Arrow, Plain text styles), LibreOffice help source validity.xhp (Data, Validity; Allow List; Input Help and Error Alert tabs; Stop, Warning, Information).
Method: documentation only; no commands were run.
