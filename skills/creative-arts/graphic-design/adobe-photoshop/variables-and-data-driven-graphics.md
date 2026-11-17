---
id: creative-arts.graphic-design.adobe-photoshop.variables-and-data-driven-graphics
name: variables-and-data-driven-graphics
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-automation, data-driven-graphics, variables, data-sets, csv, personalised-graphics]
level: advanced
status: draft
description: "Generate personalised graphics with Photoshop variables and data sets: text replacement, pixel replacement and visibility variables, CSV import and export."
sources:
  - https://helpx.adobe.com/photoshop/using/creating-data-driven-graphics.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data-driven graphics with variables

**Goal:** one template PSD, hundreds of versions (name badges, product tiles, social cards) from a spreadsheet.

## Variable types (Image > Variables > Define)
- **Text Replacement** - on a type layer; replaces text.
- **Pixel Replacement** - on a pixel layer; swaps in an image file from a path. Method: Fit,
  Fill, As Is, Conform; alignment point.
- **Visibility** - any layer; shows/hides (true/false).
Variable names: start with a letter, no spaces (`name`, `photo`, `showBadge`).

## Data file (CSV or tab-delimited TXT)
```
name,photo,showBadge
Ana Ruiz,<data-folder>/img/ana.jpg,true
Ben Okoro,<data-folder>/img/ben.jpg,false
```
- First row = variable names exactly. Pixel paths absolute (or relative to the data file in recent versions).
- Values containing commas need quotes. Save as UTF-8 for accents.

## Import and preview
Image > Variables > Data Sets > Import; step through data sets with the arrows to preview each.

## Export
File > Export > **Data Sets as Files** - one PSD per data set with naming tokens; then Image
Processor or a Batch action to convert to JPEG/PNG. (Export to PDF needs an action or script.)

## Gotchas
- Long names overflow: use paragraph text boxes and test the longest value; consider smaller font fallback rows.
- Missing image path stops the export; validate paths first.
- Excel CSV may add BOM or use semicolons in some locales.

## Verify
- [ ] Preview longest and shortest records.
- [ ] File count = row count.
