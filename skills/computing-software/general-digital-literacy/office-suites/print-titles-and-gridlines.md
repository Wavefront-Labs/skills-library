---
id: computing-software.general-digital-literacy.office-suites.print-titles-and-gridlines
name: print-titles-and-gridlines
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, spreadsheets, print-spreadsheet, print-titles, repeat-header-rows, print-gridlines, row-and-column-headings, header-footer-spreadsheet, spreadsheet-headers-footers]
level: intro
status: docs-checked
description: "Repeat header rows on every printed page, print gridlines and row/column headings, and add headers and footers to spreadsheet printouts in Excel, Sheets and Calc."
sources:
  - https://support.microsoft.com/en-us/excel/print-rows-with-column-headers-on-top-of-every-page
  - https://support.microsoft.com/en-us/excel/print-gridlines-in-a-worksheet
  - https://support.microsoft.com/en-us/excel/print-row-and-column-headings
  - https://support.google.com/docs/answer/7663148?hl=en
  - https://help.libreoffice.org/latest/en-US/text/scalc/01/05080300.html
  - https://help.libreoffice.org/latest/en-US/text/scalc/01/05070500.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Print titles and gridlines

**Goal:** every printed page of a long table is readable on its own.

## Repeat header rows
- **Excel (desktop):** **Page Layout › Page Setup › Print Titles** › *Sheet* tab › **Rows to repeat at
  top** (for example `$1:$1`) and/or **Columns to repeat at left**. Excel for the web can't repeat
  column headers when printing.
- **Google Sheets:** freeze the header row first, then **File › Print › Headers & footers › Repeat frozen
  rows** (or *Repeat frozen columns*).
- **Calc:** **Format › Print Ranges › Edit** › *Rows to repeat* (for example `$1`) and *Columns to repeat*.

## Gridlines and headings
- Excel: **Page Layout › Sheet Options** › *Gridlines* › **Print**, and *Headings* › **Print** for the
  A, B, C / 1, 2, 3 labels when someone will refer to cells.
- Calc: **Format › Page Style › Sheet** tab › *Grid* (and column and row headers).
- Or add real cell borders, which print in every app.

## Headers and footers
Google Sheets: **File › Print › Headers & footers** › choose what to include; *Edit custom fields* changes
format and position.

## Gotchas
- Print Titles is dimmed while you are editing a cell, when a chart on the sheet is selected, or when no
  printer is installed.
- With several sheets selected (grouped), the *Rows to repeat at top* box is unavailable; ungroup first.
- The Sheet Options checkboxes are dimmed while a chart, image or other object is selected.

## Verify
- [ ] Page 2 of the preview starts with the header row.

## Checked
- 2026-10-27, against Microsoft Support (Excel for Microsoft 365), Google Docs Editors Help and
  LibreOffice help (master) as published on that date: Print Titles location and boxes, the web
  limitation, dimmed-command conditions, grouped-sheet limitation, Gridlines and Headings Print
  checkboxes; Sheets Repeat frozen rows/columns and headers & footers; Calc Edit Print Ranges repeat rows
  and Page Style Sheet Grid.

Method: documentation only; no commands were run.
