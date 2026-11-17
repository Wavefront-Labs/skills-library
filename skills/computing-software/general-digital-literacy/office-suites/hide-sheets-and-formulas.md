---
id: computing-software.general-digital-literacy.office-suites.hide-sheets-and-formulas
name: hide-sheets-and-formulas
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, print-spreadsheet, protect-sheet, hide-formulas, very-hidden, hide-worksheet]
level: practitioner
status: docs-checked
description: "Hide worksheets and formulas in Excel and Google Sheets so recipients see results not workings, and understand why hiding is not security."
sources:
  - https://support.microsoft.com/en-us/office/hide-or-unhide-worksheets-69f2701a-21f5-4186-87d7-341a8cf53344
  - https://support.microsoft.com/en-us/office/display-or-hide-formulas-f7f5ab4e-bf24-4efc-8fc9-0c1b77a5356f
  - https://support.microsoft.com/en-us/excel/protect-a-workbook
  - https://support.microsoft.com/en-us/office/remove-hidden-data-and-personal-information-by-inspecting-documents-presentations-or-workbooks-356b7b5d-77af-44fe-a07f-9aa4d085966f
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hide sheets and formulas

## Hide a sheet
- Excel: right-click the tab › **Hide**; right-click any visible tab › **Unhide** lists hidden
  sheets. Other sheets and workbooks can still reference data on a hidden sheet. Lock the workbook
  structure with **Review › Protect Workbook** to stop others adding, moving, deleting, hiding and
  renaming sheets.

## Hide formulas (show results only)
1. Select the formula cells.
2. **Home › Format › Format Cells › Protection** › tick **Hidden**.
3. **Review › Protect Sheet** (password optional). The formula bar is now blank for those cells.
- Cells are Locked by default; untick Locked on input cells before protecting so people can still
  type in them.

## Gotchas
- Hidden is not secret. Data in hidden sheets, rows or columns is in the file: copy-paste, Power
  Query or a copy of the workbook reveals it, and Microsoft says worksheet protection is not a
  security feature. Delete sensitive data or send a values-only copy (copy › Paste Special Values
  into a new workbook) instead.
- A sheet set to "very hidden" with VBA is missing from the Unhide list; still not security.
- Run **File › Info › Check for Issues › Inspect Document** (on a copy: removed data may not be
  restorable) to find hidden rows, columns and sheets before sharing.

## Verify
- [ ] Recipient copy: formula bar empty on protected cells, and no sensitive data left in hidden places.

## Checked

2026-10-27. Documentation checked against the current pages listed in sources. Microsoft Hide or unhide worksheets (right-click tab, Hide and Unhide; very hidden sheets set by VBA are not listed by Unhide; hidden sheets can still be referenced), Display or hide formulas (Format Cells, Protection, Hidden, then Review, Protect Sheet), Protect a workbook (Review, Protect Workbook locks structure; worksheet protection is not a security feature), Document Inspector (File, Info, Check for Issues, Inspect Document; use on a copy).
Method: documentation only; no commands were run.
