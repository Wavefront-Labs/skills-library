---
id: creative-arts.graphic-design.adobe-indesign.table-and-cell-styles-with-alternating-fills
name: table-and-cell-styles-with-alternating-fills
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, indesign-tables, table-styles, cell-styles, alternating-fills, cell-insets, row-strokes, zebra-striping, table-design]
level: practitioner
status: draft
description: "Design InDesign tables with table and cell styles: alternating row fills, light rules instead of grids, cell insets and vertical alignment, and paragraph styles inside cells."
sources:
  - https://helpx.adobe.com/indesign/using/table-cell-styles.html
  - https://helpx.adobe.com/indesign/using/formatting-tables.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Table and cell styles with alternating fills

**Goal:** tables that read easily and can be restyled in one place, even after data updates.

## Design principles
- Fewer lines: horizontal rules or alternating fills instead of a full grid (Tufte's data-ink idea).
- Light alternating fill (5-10% tint) aids tracking along wide rows; skip it on short tables.
- Generous **cell insets** (e.g. 1-2 mm top/bottom, 2 mm left/right) and vertical alignment centre or top.
- Numbers right-aligned or decimal-aligned, text left-aligned; headers aligned like their column.

## Build the styles
1. **Paragraph styles** for cell text: `Table Body`, `Table Body Num` (right align, tabular figures), `Table Head`.
2. **Cell styles** (Window > Styles > Cell Styles): `Header Cell` (fill, bottom rule, Paragraph Style = Table Head),
   `Body Cell` (insets, paragraph style Table Body), `Total Cell` (top rule, bold). A cell style can set the
   paragraph style automatically.
3. **Table style** (Window > Styles > Table Styles): Table Setup (border), **Row Strokes** and **Fills**:
   - Fills > **Alternating Pattern: Every Other Row**, First 1 row colour (e.g. 8% tint), Next 1 row None;
     Skip First rows (headers).
   - Row strokes: e.g. 0.25 pt grey every row, or none with fills.
   - Cell Styles section: assign Header Rows, Body Rows, Left/Right Column cell styles.
4. Apply: click in the table, click the table style. Clear overrides on cells (Alt/Option+click the style).

## Updating data
Linked Excel data replaces cell contents; formatting from styles survives, local formatting does not. Keep
everything in styles (see importing Excel tables skill).

## Gotchas
- Cell styles override table style regions; local overrides override both - the + sign marks them.
- Fills in alternating pattern restart after header rows only if Skip First is set.
- Strokes: cell strokes and table strokes overlap; "Stroke Drawing Order" (Table Options) decides which shows.

## Verify
- [ ] Changing the table style updates all tables of that type.
- [ ] No local overrides in tables; numbers aligned properly.
