---
id: computing-software.general-digital-literacy.office-suites.opening-csv-files-correctly
name: opening-csv-files-correctly
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, spreadsheets, sort-and-filter, import-csv, csv, text-import, utf-8, leading-zeros, delimiter, get-data-from-text, text-encoding]
level: intro
status: docs-checked
description: "Open or import CSV files in Excel, Google Sheets and LibreOffice Calc without losing leading zeros, long IDs or column types."
sources:
  - https://support.microsoft.com/en-us/excel/get-started/import-or-export-text-txt-or-csv-files
  - https://support.microsoft.com/en-us/excel/set-automatic-data-conversions
  - https://support.microsoft.com/en-us/excel/keeping-leading-zeros-and-large-numbers
  - https://support.google.com/docs/answer/40608?hl=en
  - https://help.libreoffice.org/latest/en-US/text/shared/00/00000208.html
  - https://help.libreoffice.org/latest/en-US/text/scalc/guide/csv_files.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Opening and importing CSV files correctly

**Goal:** get a CSV into a spreadsheet with every value intact.

## The problem with double-clicking
When Excel opens a `.csv` file directly it applies its default data-format settings to every column. By
default it removes leading zeros (`00123` becomes 123), keeps only 15 digits of long numbers (showing them
in scientific notation), and reads values around the letter "E" as scientific notation.

## Import instead
- **Excel:** **Data › Get & Transform Data › From Text/CSV** › choose the file › **Import**. Pick the
  *Delimiter*, check the preview, then **Load** (or *Load To* for a table, PivotTable or connection), or
  **Transform Data** to set column types in Power Query before loading (set IDs and postcodes to Text).
- **Excel options:** **File › Options › Data › Automatic Data Conversion** lets you turn off the leading-zero,
  15-digit and "E" conversions (Excel for Microsoft 365 and Excel 2024, Windows and Mac). These options do
  not change Power Query imports.
- **Google Sheets:** **File › Import** › upload the file › choose where the data goes and the *Separator
  character* (detect automatically, tab, comma or custom).
- **LibreOffice Calc:** **File › Open** a `.csv` file to get the **Text Import** dialog: set the
  *Character set*, the separators, and click each column in the preview to choose its *Column type*
  (for example Text).

## Gotchas
- Re-saving an Excel-opened CSV keeps the converted values; don't round-trip data files that feed
  other systems through Excel unless they were imported with Text columns.

## Verify
- [ ] Spot-check a leading-zero code, a long ID, a date and an accented name after import.

## Checked
- 2026-10-27, against Microsoft Support (Excel for Microsoft 365), Google Docs Editors Help and
  LibreOffice help (master) as published on that date: default CSV conversions, From Text/CSV with
  Delimiter/Load/Load To/Transform Data, the Automatic Data Conversion options path, versions and Power
  Query note, Sheets import separator options, Calc Text Import character set and column types.

Method: documentation only; no commands were run.
