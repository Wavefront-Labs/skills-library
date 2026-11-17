---
id: computing-software.general-digital-literacy.office-suites.saving-a-sheet-as-pdf
name: saving-a-sheet-as-pdf
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, ss-output, spreadsheet-to-pdf, export-pdf, print-area]
level: intro
status: docs-checked
description: "Export a worksheet, selection or workbook to PDF from Excel or Google Sheets with sensible page breaks, scaling, repeated headers and headers/footers."
sources:
  - https://support.microsoft.com/en-us/office/collab-files/save-or-convert-to-pdf-or-xps-in-office-desktop-apps
  - https://support.microsoft.com/en-us/excel/set-or-clear-a-print-area-on-a-worksheet
  - https://support.microsoft.com/en-us/excel/scale-a-worksheet
  - https://support.microsoft.com/en-us/excel/print-rows-with-column-headers-on-top-of-every-page
  - https://support.google.com/docs/answer/7663148?hl=en
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Save a sheet as PDF

## Excel
1. Fix the layout first: **Page Layout › Print Area › Set Print Area**, **Page Layout › Page Setup ›
   Orientation**, **Print Titles** for repeating headers, and **Scale to Fit** (Width 1 page, Height
   Automatic) for wide sheets. **View › Page Break Preview** shows what lands on each page.
2. **File › Save As** (or *Save a Copy*) › *Save as type* **PDF (*.pdf)**.
3. Choose *Standard* (printing) or *Minimum size* (online), then **Options** to set which pages and
   content are published › OK › Save.

## Google Sheets
**File › Print**: choose *Current sheet*, *Workbook* or *Selected cells*, set orientation, margins,
custom page breaks and **Headers & footers** (including *Repeat frozen rows*) › **Next**. In Chrome a print
window opens; in Firefox or Safari a PDF file downloads.

## Gotchas
- Wide sheets split columns across pages unless scaled to fit the width; check every page.
- Charts outside the print area are left out; place them inside it.
- Gridlines don't print unless chosen; add borders for tables.

## Verify
- [ ] Open the PDF and page through: no orphan columns, headers repeat, numbers not showing as `#####`.

## Checked
- 2026-10-27, against Microsoft Support (Microsoft 365 desktop apps) and Google Docs Editors Help as
  published on that date: Save As / Save a Copy to PDF with Standard/Minimum size and Options, print
  area, orientation, Print Titles, Scale to Fit, Page Break Preview; Sheets print scope, layout options,
  Repeat frozen rows and the browser-dependent PDF output.

Method: documentation only; no commands were run.
