---
id: computing-software.general-digital-literacy.office-suites.table-borders-shading-and-merged-cells
name: table-borders-shading-and-merged-cells
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, word-processing, table-borders, merge-cells, split-cells, table-shading, table-styles, cell-alignment]
level: intro
status: docs-checked
description: "Style document tables with table styles, borders and shading, merge or split cells and align cell text in Word, Google Docs and LibreOffice."
sources:
  - https://support.microsoft.com/en-us/word/merge-or-split-cells-in-a-table
  - https://support.microsoft.com/en-us/accessibility/word/make-your-word-documents-accessible-to-people-with-disabilities
  - https://support.microsoft.com/en-us/office/security-privacy/set-or-change-table-properties
  - https://support.microsoft.com/en-us/word/training/print-labels-for-your-mailing-list
  - https://support.google.com/docs/answer/1696711
  - https://help.libreoffice.org/latest/en-US/text/swriter/00/00000405.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Table borders, shading and merged cells

**Goal:** a readable table: clear header, light lines, sensible alignment.

## Quick look with table styles (Word)
Click in the table › table **Design** tab (Table Design in newer versions) › pick a table style. In *Table Style Options* tick
*Header Row* and *Banded Rows* (Total Row is also available). A real header row also lets assistive
technology describe the table.

## Borders and shading by hand
- **Word:** right-click › Table Properties › **Borders and Shading** to set border style, line colour
  and width, and shading.
- **Google Docs:** select cells › toolbar Border color, Border width, Border dash and Background color.
- **LibreOffice:** Table › Properties.

## Merge and split
- Word: select adjacent cells › Table Layout › **Merge Cells** (or right-click › Merge Cells);
  Table Layout › **Split Cells** › enter columns and rows.
- Docs: select › right-click › Merge cells / Unmerge cells; right-click a cell › Split cell.
- LibreOffice: Table › Merge Cells / Split Cells.

## Alignment
Word: Table Properties › Cell › *Vertical alignment* Top, Center or Bottom. Docs: Format › Table ›
Table options › Cell › vertical alignment and padding. Numbers usually align right so digits line up;
text aligns left.

## Gotchas
- Merged or split cells make screen readers lose count of the table; merge only titles, never data
  cells, and run the Accessibility Checker to find them.
- Dark header shading needs light text with enough contrast; the Accessibility Checker flags low contrast.
- If no borders show, Table Layout › **View Gridlines** displays the cell outlines; check print preview
  to see which borders actually print.

## Verify
- [ ] Print preview shows the borders you expect and header text is legible.

## Checked
2026-10-27 against Microsoft Support (merge or split cells; accessible Word documents; table properties;
View Gridlines in the labels page; Word for Microsoft 365), Google Docs Editors Help (Add and edit tables)
and the LibreOffice help (master). Confirmed: Table Style Options Header Row/Banded Rows/Total Row, Merge
and Split Cells, Table Properties Borders and Shading and vertical alignment, Docs toolbar border tools,
merge/unmerge/split and Table options cell alignment, LibreOffice Table › Merge Cells/Split Cells and
Table › Properties, the screen-reader merged-cell warning. Removed unconfirmed Border Painter, alignment
grid and contrast-ratio figure. Method: documentation only; no commands were run.
