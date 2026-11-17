---
id: creative-arts.fashion-design.textile-and-print-design.digital-print-file-preparation
name: digital-print-file-preparation
category: creative-arts
field: fashion-design
product: textile-and-print-design
tags: [fashion-design, textile-and-print-design, digital-textile-printing, dtp, print-file-prep, textile-file-format, repeat-tile, print-resolution]
level: practitioner
status: draft
description: "Prepare files for digital textile printing: resolution at print size, repeat tile or engineered placement files, colour mode, file formats and naming the printer expects."
sources:
  - https://www.spoonflower.com/en/help/file-preparation
  - https://www.kornit.com/
  - https://www.bloomsbury.com/uk/printed-textile-design-9781350076358/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Print file resolution, size and format

**Goal:** files that print at the right size and quality without back-and-forth with the
digital printer.

## Resolution and size
- Set the document to the **actual print size** at **150-300 dpi** (many textile printers
  print at 150-300 dpi; check the spec sheet). Upscaling a small image does not add detail.
- For repeats, supply **one seamless tile** at its real size; the RIP steps it across the
  roll. Specify the repeat type (block, half-drop).
- For **engineered/placement prints**, supply each pattern piece's artwork laid out on the
  fabric width (from the marker or pattern DXF), with bleed (1-2 cm beyond the cut line).

## Colour
- Most digital textile printers accept **RGB or Lab**, converting in their RIP with fabric
  profiles; some want CMYK. Ask, and embed the profile (e.g. sRGB or Adobe RGB).
- Provide Pantone references for key colours and order a **colour chart/strike-off** on the
  final fabric.

## Formats
- TIFF (LZW compression, flattened, no alpha) is the safe standard; PNG/JPEG accepted by
  many; PDF for vector.
- Filename with print name, colourway, repeat size and dpi:
  `poppy_cw2_64x64cm_150dpi.tif`.

## Fabric width
Know the printable width (e.g. 140-150 cm, sometimes less than fabric width) and whether
the printer adds a margin or colour bar at the selvedge.

## Gotchas
- Wrong dpi metadata: a 6400 px tile marked 72 dpi prints huge; set the size properly.
- Transparent backgrounds print as white or fail; flatten on the ground colour.
- Placing engineered artwork without seam allowance bleed leaves white edges at seams.

## Verify
- [ ] Document at actual size and printer's required dpi.
- [ ] Format, colour mode and profile match the printer's spec.
- [ ] Strike-off ordered on the production fabric.
