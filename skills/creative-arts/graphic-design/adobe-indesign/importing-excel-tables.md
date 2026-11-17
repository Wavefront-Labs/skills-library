---
id: creative-arts.graphic-design.adobe-indesign.importing-excel-tables
name: importing-excel-tables
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, indesign-tables, excel-table-import, table-import-options, link-to-spreadsheet, table-styles, convert-text-to-table, data-tables]
level: practitioner
status: draft
description: "Bring Excel data into InDesign as formatted tables: import options, unformatted tables with table styles, linking so updates flow in, and converting tabbed text to tables."
sources:
  - https://helpx.adobe.com/indesign/using/creating-tables.html
  - https://helpx.adobe.com/indesign/using/importing-files-applications.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Importing Excel tables

**Goal:** spreadsheet data in a designed InDesign table that can be updated when the
numbers change, without restyling by hand.

## Place with import options
1. File > Place, tick **Show Import Options**, pick the .xlsx.
2. Choose **Sheet** and **Cell Range** (named ranges help: e.g. `A1:F40`).
3. **Formatting:** choose **Unformatted Table** - keeps the table structure but drops Excel
   fonts and colours, so your table style applies cleanly. "Formatted Table" drags in Excel
   styling you then have to fight. "Unformatted Tabbed Text" if you will convert yourself.
4. Table: choose your **table style** in the dialog if offered (newer versions) or apply
   afterwards.
5. Number of decimal places to show: Excel's displayed format is imported as text - round in
   Excel first.

## Keep it linked
Preferences > File Handling > **Create Links When Placing Text and Spreadsheet Files**.
Then the table appears in the Links panel; when the .xlsx changes, the link shows modified
and **Update Link** refreshes the data.
- Updating a link **replaces local formatting** inside the table; only formatting that comes
  from table/cell/paragraph styles survives. This is why styles matter.

## Apply design with styles
- Table style (borders, alternating fills, header rows) + cell styles (header cell,
  body cell, total cell) + paragraph styles in cells (right-aligned figures). See the table
  and cell styles skill.

## Converting text to a table
Tabbed or comma text already in InDesign: select it, Table > Convert Text to Table, column
separator Tab, row separator Paragraph.

## Gotchas
- Merged cells in Excel import as merged; hidden columns are skipped.
- Very long tables: the table breaks across frames; set repeating header rows.
- Formulas do not come across, only results.
- CSV via Place imports as text; convert it to a table.

## Verify
- [ ] Links panel shows the spreadsheet; Update Link refreshes values without losing styling.
- [ ] Numbers match the source (spot-check totals) and use the intended decimal places.
