---
id: creative-arts.comics-and-sequential-art.page-layout-and-pencilling.scanning-and-delivering-pencils
name: scanning-and-delivering-pencils
category: creative-arts
field: comics-and-sequential-art
product: page-layout-and-pencilling
tags: [page-layout-and-pencilling, pencilling, pencil-finishes, scanning-pencils, pencil-scan, greyscale-scan, levels-adjustment, file-naming]
level: practitioner
status: draft
description: "Scan pencilled pages for inkers, editors or blue-line printing: greyscale resolution, stitching 11x17 boards on letter scanners, levels clean-up, and naming/delivery."
sources:
  - https://openlibrary.org/search?q=DC+Comics+Guide+to+Pencilling+Comics
  - https://helpx.adobe.com/photoshop/using/levels-adjustment.html
  - https://en.wikipedia.org/wiki/Non-photo_blue
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scanning and delivering pencils

**Goal:** clean, consistent digital pencils the next person can work from.

## Scan settings
- **Greyscale**, 8-bit; pencils need tonal range (not 1-bit).
- **Resolution**: 300-400 dpi at original size for review/blue-lines; 600 dpi if the
  inker inks digitally over them or they'll be printed as pencils.
- Disable scanner "auto" sharpening/descreen; you'll adjust levels yourself.

## Large boards on small scanners
11x17 boards don't fit A4/letter flatbeds. Scan in two overlapping halves (keep the
board square to the glass), then merge in Photoshop (File > Automate > Photomerge,
layout "Reposition") or align manually with layer difference blending.

## Clean-up
1. Crop to the board's bleed marks; straighten (Image > Image Rotation or ruler tool).
2. **Levels**: move the white point left until the paper is pure white; darken the
   black point/midtones slightly so light lines survive.
3. Remove non-photo-blue roughs if needed: use the Channels (keep the blue channel,
   which drops blue to white) or Hue/Saturation targeting cyan/blue with lightness up.
4. Spot-heal dust and eraser crumbs.

## Delivery
- File naming: `TITLE_##_p07_pencils.tif` (zero-padded page numbers sort correctly).
- Format: TIFF (LZW) or high-quality JPEG for review; PSD only if requested.
- Upload to the agreed shared folder; send the page list in the message.

## Verify
- [ ] Paper pure white, lines intact, consistent darkness across pages.
- [ ] Correct resolution and size for the recipient.
- [ ] Files named and sorted by page.
