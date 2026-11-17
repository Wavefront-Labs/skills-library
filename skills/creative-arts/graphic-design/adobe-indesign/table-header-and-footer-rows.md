---
id: creative-arts.graphic-design.adobe-indesign.table-header-and-footer-rows
name: table-header-and-footer-rows
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, indesign-tables, table-header-rows, footer-rows, repeating-headers, table-breaks, keep-rows-together, long-tables]
level: practitioner
status: draft
description: "Make long InDesign tables readable across frames and pages: header and footer rows that repeat, where rows may break, keep options and continued labels."
sources:
  - https://helpx.adobe.com/indesign/using/formatting-tables.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Table header and footer rows

**Goal:** a table that flows over several columns or pages and still tells the reader what every column means.

## Convert rows to headers/footers
- Select the top row(s), Table > Convert Rows > **To Header**. Select bottom row(s) > To Footer.
- Or Table > Table Options > **Headers and Footers**: Header Rows count, **Repeat Header:** Every Text Column /
  Once per Frame / Once per Page; same for footers; **Skip First** (header) / Skip Last (footer) - e.g. a footer
  "continued" that should not appear at the end.
- Header rows are edited only in their first instance; repeats update automatically.

## Breaking behaviour
- A table lives in one text frame thread; it breaks to the next frame/column when it does not fit.
- **Row height:** "At Least" lets rows grow with text; "Exactly" clips content (overset cell shows a red dot).
- Cell Options > Rows and Columns > **Keep Options:** Start Row (Anywhere, Next Column, Next Frame, Next Page) and
  **Keep with Next Row** - keep subtotal rows with their group, keep first data rows with headers.
- Avoid splitting a single tall row: rows cannot split across frames unless "Allow Row to Break Across Frames" is on
  (CC 2014+ in Cell Options).

## "Continued" labels
Put "continued" text in a footer row with Skip Last, or in a header row with Skip First ("Table 3 (continued)").

## Styling
Header rows get their own cell style (`Table Header`), set in the **table style** Header Rows region, so they look
the same in every repeat (see table and cell styles).

## Gotchas
- Converting rows imported from Excel to headers after styling may change their cell style - reapply the table style.
- Tables inside anchored frames do not flow; keep long tables in the main story.
- Accessibility: header rows map to TH cells in tagged PDF and EPUB - another reason to convert them properly.

## Verify
- [ ] Every continuation of the table starts with the header row(s).
- [ ] No overset cells (red dots); grouped rows stay together.
