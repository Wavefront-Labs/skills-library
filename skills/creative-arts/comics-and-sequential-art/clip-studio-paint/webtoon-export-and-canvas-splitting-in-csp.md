---
id: creative-arts.comics-and-sequential-art.clip-studio-paint.webtoon-export-and-canvas-splitting-in-csp
name: webtoon-export-and-canvas-splitting-in-csp
category: creative-arts
field: comics-and-sequential-art
product: clip-studio-paint
tags: [clip-studio-paint, csp-export, csp-webtoon-export, webtoon-canvas, image-slicing, vertical-scroll, export-webtoon]
level: practitioner
status: draft
description: "Export vertical webtoon episodes from Clip Studio Paint: webtoon canvas setup, File > Export webtoon, output width, split height, file naming and checking slices."
sources:
  - https://www.webtoons.com/en/creators101/webtoon-canvas
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Webtoon export and canvas splitting

## Canvas
- File > New, use the **Webtoon** project type (recent versions): set width (e.g. 800 px for WEBTOON
  CANVAS, or 1600 px for 2x working size), a long height, and optionally split into pages per
  episode in a story.
- Canvas height can be extended later (Edit > Change canvas size) while drawing.

## Export
- **File > Export webtoon** (newer versions; older versions use Export multiple pages with split options or
  manual slicing):
  - **Output width** - scale to the platform width (WEBTOON CANVAS: 800 px).
  - **Divide** - by height per image (WEBTOON allows up to 1280 px tall per image; Tapas similar limits),
    yielding numbered slices.
  - File format JPEG/PNG, quality, colour profile sRGB.
  - File name prefix and numbering ("ep12_01.jpg").
- Check the platform's current limits for slice height, file size (WEBTOON: under 2 MB per image,
  total per episode under 20 MB) and count.

## Check
- Slice boundaries that cut through faces or text are fine for continuous scroll, but some readers on
  slow connections see partial loads; nudge splits into gutters if your export allows custom split points.
- Re-assemble preview: upload to the platform's preview or view slices stacked in a browser.

## Gotchas
- Exporting at 1600 px without scaling exceeds limits on some platforms.
- RGB profile mismatches give dull colours; export sRGB.
- Text sized for the 1600 px canvas halves on export; size accordingly.

## Verify
- [ ] Every slice within platform limits; preview shows no gaps or duplicated rows.
