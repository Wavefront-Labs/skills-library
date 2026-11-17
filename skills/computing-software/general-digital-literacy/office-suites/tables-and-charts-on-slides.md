---
id: computing-software.general-digital-literacy.office-suites.tables-and-charts-on-slides
name: tables-and-charts-on-slides
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, presentations, slide-charts, slide-tables, powerpoint, google-slides, linked-chart, copy-chart]
level: intro
status: docs-checked
description: "Add readable tables and charts to PowerPoint, Google Slides and Impress slides, edit their data, link them to a spreadsheet, and keep them simple enough to read from the back."
sources:
  - https://support.microsoft.com/en-us/office/use-charts-and-graphs-in-your-presentation-c74616f1-a5b2-4a37-8695-fbcc043bf526
  - https://support.microsoft.com/en-us/office/insert-and-update-excel-data-in-powerpoint-0690708a-5ce6-41b4-923f-11d57554138d
  - https://support.microsoft.com/en-us/office/change-the-data-in-an-existing-chart-539c9840-7412-4da3-ab06-fcf318e996df
  - https://support.microsoft.com/en-us/powerpoint/what-is-a-slide-layout
  - https://support.microsoft.com/en-us/accessibility/powerpoint/make-your-powerpoint-presentations-accessible-to-people-with-disabilities
  - https://support.google.com/docs/answer/7009814
  - https://github.com/LibreOffice/help/blob/master/source/text/simpress/00/00000404.xhp
  - https://github.com/LibreOffice/help/blob/master/source/text/shared/00/00000404.xhp
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Tables and charts on slides

**Goal:** one clear point per table or chart that the back row can read.

## PowerPoint
- **Insert › Table** for a table; keep it small and split big tables or move detail to a handout.
- **Insert › Chart** › pick a type, then replace the sample worksheet data with yours. Later: **Chart Design ›
  Edit Data** (works for embedded and linked charts).
- Existing Excel chart: copy it in Excel, paste in PowerPoint, then **Paste Options** › *Use Destination Theme &
  Link Data* (or *Keep Source Formatting & Link Data*) to keep it linked to the workbook. For large or
  frequently changing data, Microsoft suggests building the chart in Excel and linking it.
- Content placeholders on a layout can hold tables and charts sized to the layout.

## Google Slides
- **Insert › Chart** › a chart type creates a chart linked to a new Google Sheet; **Insert › Chart › From Sheets**
  links an existing chart (clear *Link to spreadsheet* for a static copy).
- Tables: copy cells in Sheets, paste in Slides and choose *Link to spreadsheet* or *Paste unlinked* (tables over
  400 cells paste unlinked).
- When the sheet changes, click **Update** on the chart or table, or Tools › **Linked objects** › Update all;
  **Link options › Unlink** freezes it.

## LibreOffice Impress
Insert › Table / Insert › Chart; Insert › OLE Object for an embedded spreadsheet.

## Design rules
- Title states the takeaway ("Sales doubled in Q3"), not "Sales chart".
- Use large fonts; remove gridlines and 3-D effects; label data directly instead of a far-away legend.
- Highlight the one bar or row that matters in a contrasting colour; mute the rest.
- Add alt text summarising the finding. Microsoft's accessibility guidance says to avoid tables where you can
  and keep any table a simple data grid with column headers.

## Gotchas
- A linked chart needs the source workbook; if you send the deck without it, check the chart still shows what
  you expect, or paste a static copy.
- Updating a linked Google chart overwrites edits made to it in Slides.

## Verify
- [ ] Slide shows from a few metres away: every label readable.
- [ ] Linked charts update (or are deliberately frozen) before presenting.

## Checked
2026-10-27, against Microsoft Support (Use charts and graphs in your presentation; Insert and update Excel data; Change the data in an existing chart; slide layouts; accessibility guide; PowerPoint for Microsoft 365 and 2016-2024), Google Docs Editors Help (Link a chart, table or slides) and the LibreOffice help master branch (Impress and shared Insert menus). Confirmed: Insert › Chart and sample data, Chart Design › Edit Data, the link Paste Options, layout placeholders for tables and charts, Google chart/table linking, the 400-cell limit, Update, Linked objects and Unlink, the overwrite note, Impress Insert › Table/Chart/OLE Object, and Microsoft's table guidance. Corrected "right-click › Edit Data" and "Paste Special" to the documented commands; removed an unconfirmed chart-animation option, size rules and a Google Insert › Table path.
Method: documentation only; no commands were run.
