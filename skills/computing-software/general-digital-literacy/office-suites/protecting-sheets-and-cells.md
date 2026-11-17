---
id: computing-software.general-digital-literacy.office-suites.protecting-sheets-and-cells
name: protecting-sheets-and-cells
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, spreadsheets, print-spreadsheet, protect-sheet, lock-cells, protect-workbook, protected-ranges, password-to-open]
level: intro
status: docs-checked
description: "Lock formula cells while leaving input cells editable, protect sheets and workbook structure, and know what spreadsheet protection does and does not secure."
sources:
  - https://support.microsoft.com/en-us/excel/protect-a-worksheet
  - https://support.microsoft.com/en-us/excel/lock-cells-to-protect-them-in-excel
  - https://support.google.com/docs/answer/1218656
  - https://github.com/LibreOffice/help/blob/master/source/text/scalc/guide/cell_protect.xhp
  - https://github.com/LibreOffice/help/blob/master/source/text/shared/guide/protection.xhp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Protecting sheets and locking cells

**Goal:** people can type in the input cells but can't overwrite formulas.

## Excel
1. All cells are "Locked" by default but locking only applies once the sheet is protected.
2. Select the input cells › `Ctrl+1` › Protection › **untick Locked**.
3. Review › **Protect Sheet** › choose what users may still do › optional password. Without a
   password, any user can unprotect the sheet.
4. Review › **Protect Workbook** locks the sheet structure.
5. To keep the whole file private: File › Info › Protect Workbook › **Encrypt with Password**
   (password to open). Microsoft says sheet protection is not a security feature.

## Google Sheets
Data › **Protect sheets and ranges** › add a sheet or range › Set permissions: *Show a warning when
editing this range* (editors confirm each change) or *Restrict who can edit this range* (Only you,
Only domain, or Custom).

## LibreOffice Calc
Select the cells › Format › Cells and set the protection options (they apply only after the sheet is
protected) › **Tools › Protect Sheet** (or **Tools › Protect Spreadsheet Structure**). File ›
Save As › *Save with password* to protect the whole document.

## Gotchas
- Sheet protection stops accidents, not determined users.
- Lost the "open" password of an encrypted file? Microsoft cannot retrieve it. Store it in a
  password manager.

## Verify
- [ ] Try typing over a formula: blocked. Typing in an input cell: works.

## Checked

2026-10-27. Documentation checked against the current pages listed in sources. Microsoft Protect a worksheet and Lock cells pages (cells are locked by default but locking only works once the sheet is protected; Format Cells, Protection; Review, Protect Sheet; password optional; not a security feature), Google Sheets help (Data, Protect sheets and ranges; Show a warning when editing or Restrict who can edit), LibreOffice help sources (Format, Cells for protection options; Tools, Protect Sheet and Protect Spreadsheet Structure; Save with password in the Save dialog).
Method: documentation only; no commands were run.
