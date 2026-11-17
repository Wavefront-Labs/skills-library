---
id: computing-software.general-digital-literacy.office-suites.repeat-table-header-rows-and-autofit
name: repeat-table-header-rows-and-autofit
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, document-tables, repeat-header-row, autofit-table, table-properties, row-breaking]
level: practitioner
status: docs-checked
description: "Make a Word table's header row repeat on every page, stop rows splitting across pages, and set AutoFit so tables fit the page width."
sources:
  - https://support.microsoft.com/en-us/word/repeat-table-header-on-subsequent-pages
  - https://support.microsoft.com/en-us/office/security-privacy/set-or-change-table-properties
  - https://support.microsoft.com/en-us/word/resize-a-table-column-or-row
  - https://support.google.com/docs/answer/1696711
  - https://help.libreoffice.org/latest/en-US/text/swriter/01/05090300.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Repeat table header rows and AutoFit

## Repeat the header row (Word)
1. Select the header row(s) (the selection must include the first row of the table).
2. **Table Layout › Data › Repeat Header Rows**, or right-click › **Table Properties › Row** › tick
   *Repeat as header row at the top of each page*.
- Google Docs: Format › Table › **Table options** › Row › *Pin header row(s)* and the number of rows
  (or right-click a row › Pin header up to this row).
- LibreOffice: Table Properties › Text Flow › *Repeat heading*.

## Stop rows splitting
- Word: **Table Properties › Row** › under *Options*, clear the setting that allows the row to break
  across pages (the whole row then moves to the next page).
- Google Docs: Table options › Row › untick *Allow row to overflow across pages* (pages format only).
- LibreOffice: Table Properties › Text Flow › untick *Allow row to break across pages and columns*.

## AutoFit (Word: Table Layout › Cell Size › AutoFit)
- **AutoFit Contents**: columns shrink/grow to content (good for narrow data).
- **AutoFit Window**: table spans the page width (good default).
- **Fixed Column Width**: turns AutoFit off so columns stay put. Use for forms.
- Equalise: select columns › **Distribute Columns**.

## Gotchas
- Repeated headers show only in Print Layout view or when printed.
- Word repeats headers only at automatic page breaks, not after a manual page break inside the table.
- Only the header on the first page can be edited; the repeats update from it.
- A table pasted from a web page often has fixed widths wider than the page; apply AutoFit Window.

## Verify
- [ ] Print preview: header row appears at top of page 2+, and no row is cut in half.

## Checked
2026-10-27 against Microsoft Support Word table pages (Word for Microsoft 365, 2024, 2021), Google Docs
Editors Help (Add and edit tables) and the LibreOffice help (master). Confirmed: Repeat Header Rows and
the Table Properties Row option, row-break options in all three apps, AutoFit Contents/Window/Fixed Column
Width, Distribute Columns, Print Layout and manual-break limits. Corrected the Docs path to Table options.
Removed unconfirmed screen-reader and text-wrapping claims. Method: documentation only; no commands were run.
