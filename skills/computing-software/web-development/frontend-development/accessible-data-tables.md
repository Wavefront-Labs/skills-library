---
id: computing-software.web-development.frontend-development.accessible-data-tables
name: accessible-data-tables
category: computing-software
field: web-development
product: frontend-development
tags: [semantic-html, html-tables, table-headers-scope, caption, data-tables, accessibility, wcag-1-3-1]
level: practitioner
status: docs-checked
description: "Marking up data tables with caption, thead, th scope, headers/id for complex grids, and colgroup, so screen readers announce the right header for every cell."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Element/table
  - https://www.w3.org/WAI/tutorials/tables/
  - https://html.spec.whatwg.org/multipage/tables.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Accessible data tables

**Goal:** when a screen reader moves to any cell it announces the row and column headers, and the table has a name.

## 1. Simple table
```html
<table>
  <caption>Q3 revenue by region (USD thousands)</caption>
  <thead>
    <tr><th scope="col">Region</th><th scope="col">July</th><th scope="col">August</th></tr>
  </thead>
  <tbody>
    <tr><th scope="row">EMEA</th><td>420</td><td>455</td></tr>
  </tbody>
</table>
```
- `<caption>`, a direct child of `<table>`, acts as the table's heading; screen readers announce it. Alternatively point `aria-labelledby` on the table at a visible heading.
- `scope="col"`/`"row"` remove ambiguity; first-column row headers are `<th scope="row">` too.

## 2. Grouped headers
- Header spanning columns: `<th colspan="2" scope="colgroup">` with `<colgroup span="2">` defined.
- Header spanning rows: `scope="rowgroup"` on the `<th>`.

## 3. Irregular/complex tables
When headers do not line up with scope, give every `<th>` an `id` and list them on each cell: `<td headers="h-q3 h-emea h-rev">`.

## 4. Do not
- Use tables for layout; use CSS for visual presentation.
- Use `<div>` grids for tabular data - you lose all header association. If CSS changes the display of table elements, test with a screen reader that table semantics survive.
- Rely on obsolete table attributes; put explanation in `<caption>` or a linked paragraph.

## Verify
- Move through the table with a screen reader's table navigation and check each cell announces its row and column headers.
- Run an automated accessibility checker on the page.

## Checked
2026-10-28. Confirmed on the W3C WAI tables tutorial pages (overview, caption and summary, irregular, multi-level): caption as child of table, `aria-labelledby` on a table, `scope` values including colgroup and rowgroup, `<colgroup span>`, `headers`/`id` for multi-level tables, tables not for layout; MDN confirms obsolete presentational attributes. Removed: the split-into-simpler-tables advice, `role="presentation"` layout advice, the ARIA grid remark, caption-first-child rule, Safari behaviour, screen-reader key combinations and axe rule ids.
Method: documentation only; no commands were run.
