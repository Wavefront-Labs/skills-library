---
id: computing-software.general-digital-literacy.office-suites.watermarks-and-page-colour
name: watermarks-and-page-colour
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, document-images, watermark, draft-watermark, page-colour, page-borders]
level: intro
status: docs-checked
description: "Add a DRAFT or CONFIDENTIAL text watermark or a picture watermark in Word or Google Docs, remove one, and set page colour and borders."
sources:
  - https://support.microsoft.com/en-us/word/watermarks-in-word
  - https://support.microsoft.com/en-us/word/remove-a-watermark
  - https://support.microsoft.com/en-us/word/insert-a-picture-watermark
  - https://support.microsoft.com/en-us/word/add-change-or-delete-the-background-color-in-word
  - https://support.microsoft.com/en-us/word/word-options-display
  - https://support.microsoft.com/en-us/word/training/add-a-border-to-a-page
  - https://support.google.com/docs/answer/11560109
  - https://support.google.com/docs/answer/10296604
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Watermarks and page colour

## Word
- **Design › Watermark** › pick a preset (e.g. DRAFT), or **Custom Watermark** › Text, or Picture
  (keep *Washout* ticked so the image is faded behind the text).
- Remove: **Design › Watermark › Remove Watermark**. If it will not go, double-click near the top of
  the page to open the header, select the watermark and press Delete; repeat as needed (each section or
  first-page header can hold its own).
- Page colour: **Design › Page Color**. Prints only if File › Options › Display › *Print background
  colors and images* is ticked.
- Page borders: **Design › Page Borders**; *Apply to: This section - First page only* for a title page.
  Borders apply per section.
- Watermarks work best in desktop Word rather than the web or mobile apps.

## Google Docs
**Insert › Page elements › Watermark** › Image or Text › format in the side panel › Done. It repeats on
every page; remove it from the same panel with *Remove watermark*. Watermarks need pages format (they are
hidden in pageless). Page colour: **File › Page setup › Page color**.

## Gotchas
- A watermark is a visual label, not protection; anyone can remove it. For control, use sharing
  permissions or a protected PDF.
- Picture watermarks add to file size; compress the image first.
- State confidentiality in the body text too if it matters; do not rely on the watermark alone.

## Verify
- [ ] Every page (including first-page and new sections) shows the watermark in print preview / PDF.

## Checked
2026-10-27 against Microsoft Support Word watermark, page colour, Word Options (Display) and page border
pages (Word for Microsoft 365, 2024, 2021) and Google Docs Editors Help (watermarks; page settings).
Confirmed: Design › Watermark, Custom/picture Washout, Remove Watermark and the header fallback, Page
Color and the background printing option, Page Borders First page only, Docs Insert › Page elements ›
Watermark, Remove watermark, pageless limitation and Page setup page colour. Corrected the Docs menu path.
Removed unconfirmed text-watermark option names and a screen-reader claim.
Method: documentation only; no commands were run.
