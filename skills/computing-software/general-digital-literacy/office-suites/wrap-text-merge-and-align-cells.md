---
id: computing-software.general-digital-literacy.office-suites.wrap-text-merge-and-align-cells
name: wrap-text-merge-and-align-cells
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, spreadsheets, cell-formatting, wrap-text, merge-and-center, center-across-selection, cell-alignment, text-rotation, line-break-in-cell]
level: intro
status: docs-checked
description: "Wrap long text, add line breaks in a cell, merge or centre across cells and align and rotate text in Excel and LibreOffice Calc."
sources:
  - https://support.microsoft.com/en-us/excel/start-a-new-line-of-text-inside-a-cell-in-excel
  - https://support.microsoft.com/en-us/excel/fix-data-that-is-cut-off-in-cells-in-excel-for-mac
  - https://support.microsoft.com/en-us/excel/get-started/merge-and-unmerge-cells-in-excel
  - https://support.microsoft.com/en-us/excel/change-the-column-width-and-row-height
  - https://support.google.com/docs/answer/3540681?hl=en
  - https://help.libreoffice.org/latest/en-US/text/scalc/04/01020000.html
  - https://help.libreoffice.org/latest/en-US/text/scalc/01/MergeCellsMenu.html
  - https://help.libreoffice.org/latest/en-US/text/scalc/00/00000405.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wrap text, merge and align cells

**Goal:** headings and long text that fit and line up.

## Wrap and line breaks
- Excel: **Home › Wrap Text**. If wrapped text is still cut off, the row has a fixed height: **Home ›
  Format › AutoFit Row Height**.
- New line inside a cell: `Alt+Enter` (Excel for Windows), `Control+Option+Return` (Excel for Mac),
  `Ctrl+Enter` (LibreOffice Calc).
- Calc alignment and wrapping options: **Format › Cells** (`Ctrl+1`) › *Alignment* tab.

## Alignment and rotation (Excel)
Format Cells › Alignment: *Horizontal* (including **Center Across Selection**), *Vertical*, indent, and
*Orientation* (drag to an angle or type degrees) for narrow column headings. Text rotation is not
available with Fill or Center Across Selection.

## Merge vs centre across selection
- **Home › Merge & Center** (arrow for *Merge Across*, *Merge Cells*, *Unmerge Cells*) in Excel;
  **Format › Merge and Unmerge Cells** in Calc. Fine for a title above a printed report.
- Inside data, prefer **Center Across Selection**: it looks centred but keeps cells separate, so sorting,
  filtering and selecting columns still work.

## Gotchas
- Merging keeps only the upper-left cell's contents; the others are deleted. Copy anything you need first.
- Merge & Center is unavailable while you are editing a cell or inside an Excel table.
- In Google Sheets, merged cells can stop you creating a filter; unmerge first.

## Verify
- [ ] You can sort and filter the data range without merge errors.

## Checked
- 2026-10-27, against Microsoft Support (Excel for Microsoft 365 and Excel for Mac), Google Docs Editors
  Help and LibreOffice help (master) as published on that date: Wrap Text and AutoFit Row Height, line
  break keys per platform, Center Across Selection and rotation limits, Orientation, Merge & Center
  options and data loss, Merge disabled cases, Calc Merge and Unmerge Cells and Format › Cells ›
  Alignment, Sheets merged cells blocking filters.

Method: documentation only; no commands were run.
