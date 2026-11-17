---
id: creative-arts.graphic-design.adobe-indesign.data-merge-from-csv
name: data-merge-from-csv
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, indesign-automation, data-merge, csv, variable-data, business-cards, name-badges, image-fields, multiple-records, utf-16]
level: practitioner
status: draft
description: "Produce variable documents (cards, badges, certificates) with InDesign Data Merge from CSV: image and QR fields, multiple records per page, encoding fixes."
sources:
  - https://helpx.adobe.com/indesign/using/data-merge.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data merge from CSV

**Goal:** 500 name badges or business cards from one template and a spreadsheet, error-free.

## Prepare the data
- Export from Excel/Sheets as **CSV UTF-8** or **Unicode text (tab-delimited)**. Older
  InDesign versions read UTF-16 LE text more reliably than UTF-8 for accents and non-Latin
  scripts; if accents break, re-save as UTF-16.
- First row = field names, no duplicates, no special characters.
- **Image fields:** the column name starts with `@` (e.g. `@photo`), values are full paths
  (`<drive>:\badges\img\anna.jpg` on Windows, `/<folder>/badges/img/anna.jpg` on Mac) or
  paths relative to the data file in recent versions.
- QR codes: a field name starting with `#` (InDesign 2019+) generates QR codes.
- Clean data: trim spaces, check empty rows (they produce blank records).

## Build the template
1. Design one record. Put text frames and image frames where fields go.
2. Window > Utilities > Data Merge > panel menu > **Select Data Source**.
3. Click into text and click a field name to insert `<<FirstName>>`; select an image frame and
   click an image field. Style the placeholders with paragraph/character styles.
4. Image frames: set Frame Fitting Options beforehand (fill proportionally); the merge
   options also offer fitting.
5. Tick **Preview** to step through records.

## Merge (Create Merged Document)
- **Records per Document Page:** Single Record or **Multiple Records** (imposes many cards per
  sheet; set margins and spacing in the Multiple Record Layout tab).
- Remove Blank Lines for Empty Fields (for optional address lines).
- Generate Overset Text Report on - check it.
- Output to a new document (up to a record limit per document) or directly to PDF.

## Gotchas
- Updating the CSV: Data Merge panel > Update Data Source; the template keeps fields if names match.
- Multiple records per page needs the record on the first page in the top-left; misplaced
  objects outside the record area are repeated incorrectly.
- Long names overflow: use auto-sizing frames or a GREP style / smaller fallback design;
  always read the overset report.

## Verify
- [ ] Record count in output equals data rows.
- [ ] Overset report empty; accents and special characters render correctly.
- [ ] Spot-check first, last and longest-name records.
