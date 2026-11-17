---
id: computing-software.general-digital-literacy.office-suites.page-setup-margins-and-orientation
name: page-setup-margins-and-orientation
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, word-processing, page-setup, margins, orientation, landscape, paper-size, a4, us-letter, google-docs-page-setup, pageless]
level: intro
status: docs-checked
description: "Set margins, portrait or landscape orientation and paper size (A4 vs Letter) in Word, Google Docs and LibreOffice, including landscape for one page only."
sources:
  - https://support.microsoft.com/en-us/word/training/change-margins
  - https://support.microsoft.com/en-us/word/training/change-page-orientation-to-landscape-or-portrait
  - https://support.google.com/docs/answer/10296604
  - https://support.google.com/docs/answer/11528737
  - https://help.libreoffice.org/latest/en-US/text/swriter/guide/pageorientation.html
  - https://help.libreoffice.org/latest/en-US/text/swriter/guide/header_footer.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Page setup: margins, orientation and paper size

**Goal:** the printed or PDF page has the right size and white space.

## Where
- **Word:** Layout › Margins (presets or **Custom Margins**) and Layout › Orientation. Word pages start
  with one-inch margins.
- **Google Docs:** File › Page setup › **Pages** (orientation, paper size, margins, page color; *Set as
  default* applies them to new docs) or **Pageless** (continuous scroll, good for on-screen docs).
  Page setup, headers, page numbers and columns need pages format; switch with Format › Switch to Pages
  format.
- **LibreOffice Writer:** Format › Page Style.

## Paper size matters
- The common paper sizes are **A4** and **Letter**, and which one is standard depends on the region.
  A document set up for one and printed on the other is clipped or scaled. Match the recipient's region.

## One landscape page in a portrait document
- **Word:** select the wide content › Layout › open the Page Setup dialog › Landscape › Apply to:
  **Selected text**.
- **Google Docs:** select the text or image › right-click › **Change page to landscape**. Or add section
  breaks (Insert › Break › Section break) › File › Page setup › Apply to: **This section**.
- **LibreOffice:** Insert › More Breaks › Manual Break › Page break with the *Landscape* page style, then
  another manual break back to *Default Page Style*.

## Gotchas
- Very narrow margins can be cut off by home printers; check print preview.
- Headers and footers sit in the top and bottom margins; if they collide with text, increase the margin.

## Verify
- [ ] Print preview shows the right page size and nothing clipped.

## Checked
2026-10-27 against Microsoft Support (Change margins; Change page orientation, Word for Microsoft 365),
Google Docs Editors Help (page settings; pages or pageless) and the LibreOffice help (master). Confirmed:
Word Margins/Orientation and Apply to Selected text; Docs Page setup tabs, Set as default, pageless
limits, Change page to landscape and section Apply to; LibreOffice Landscape page style via Manual Break.
Corrected the Docs per-selection method. Removed unconfirmed paper dimensions, Word default-size steps and
margin figures. Method: documentation only; no commands were run.
