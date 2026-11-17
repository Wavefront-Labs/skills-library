---
id: computing-software.general-digital-literacy.office-suites.print-area-and-fit-to-page
name: print-area-and-fit-to-page
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, spreadsheets, print-spreadsheet, print-area, fit-to-page, page-break-preview, scaling, landscape]
level: intro
status: docs-checked
description: "Print only the part of a spreadsheet you need on the right number of pages using print area, fit-to-page scaling, landscape and page break preview."
sources:
  - https://support.microsoft.com/en-us/excel/set-or-clear-a-print-area-on-a-worksheet
  - https://support.microsoft.com/en-us/excel/scale-a-worksheet
  - https://support.google.com/docs/answer/7663148?hl=en
  - https://help.libreoffice.org/latest/en-US/text/scalc/00/00000405.html
  - https://help.libreoffice.org/latest/en-US/text/scalc/01/05070500.html
  - https://help.libreoffice.org/latest/en-US/text/scalc/01/03100000.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Print area and fit to page

**Goal:** a spreadsheet printout that isn't 14 pages with one column each.

## Excel
1. Select the range › **Page Layout › Print Area › Set Print Area**. Hold `Ctrl` to pick several areas
   (each prints on its own page); *Add to Print Area* extends it.
2. **Page Layout › Orientation › Landscape** for wide sheets.
3. **Page Layout › Scale to Fit**: Width **1 page**, Height **Automatic** puts all columns on one page
   and lets rows run onto more pages. Check the *Scale* box: a low number means small print.
4. **View › Page Break Preview** shows the print areas and page breaks.
5. To remove scaling: **File › Print › Settings › No Scaling**.

## Google Sheets
**File › Print**: choose *Current sheet*, *Workbook* or *Selected cells*; set *Orientation* (Landscape)
and margins; **Set custom page breaks** to drag breaks, then *Confirm breaks*.

## LibreOffice Calc
**Format › Print Ranges › Define**. **Format › Page Style › Sheet** tab › *Scaling mode*: **Shrink print
range(s) to width/height** sets the maximum pages across and down (clear one box to let that direction
use as many pages as needed). **View › Page Break** shows breaks and print ranges.

## Gotchas
- Fitting a large sheet onto one page gives unreadable text; fit the width only, or print a filtered or
  summarised view.
- The print area is saved with the workbook; clear it (Page Layout › Print Area › Clear Print Area) when
  the sheet grows.

## Verify
- [ ] Preview shows all needed columns on each page at readable size.

## Checked
- 2026-10-27, against Microsoft Support (Excel for Microsoft 365), Google Docs Editors Help and
  LibreOffice help (master) as published on that date: Set/Add to/Clear Print Area and saving with the
  workbook, Ctrl for multiple areas, Scale to Fit Width/Height, orientation, No Scaling, Page Break
  Preview; Sheets print scope, orientation and custom page breaks; Calc Print Ranges › Define, Shrink
  print range(s) to width/height, View › Page Break.

Method: documentation only; no commands were run.
