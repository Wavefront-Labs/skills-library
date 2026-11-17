---
id: creative-arts.photography-fine-art.adobe-lightroom.print-adjustment-brightness-and-contrast
name: print-adjustment-brightness-and-contrast
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, print-adjustment, lightroom-print-module, print-too-dark, print-matching, lightroom-classic]
level: practitioner
status: draft
description: "Use Lightroom Classic Print Adjustment brightness and contrast to compensate for prints that come out darker than the screen, without changing the master edit."
sources: ["https://helpx.adobe.com/lightroom-classic/help/print-module-basics.html", "https://helpx.adobe.com/lightroom-classic/desktop/help/printing-photos-basic-workflow.html", "Jeff Schewe, The Digital Print (Peachpit) - matching prints to display"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Print adjustment: brightness and contrast

Print Job panel > Color Management > **Print Adjustment** (available when Profile is a custom ICC profile, not Managed by Printer).

## Why prints look dark
- A display at 160+ cd/m2 is far brighter than paper under room light; reflective prints have less dynamic range, especially matte.
- First fix the root cause: calibrate the display to ~80-120 cd/m2 and view prints under a D50 viewing booth or 4000-5000 K high-CRI light at suitable intensity.

## Using Print Adjustment
1. Make a test print. If shadows are blocked and the print is uniformly dark, set **Brightness +5 to +15**.
2. If the print looks flat compared to screen, add **Contrast +5 to +10**.
3. Re-print and compare under the viewing light. Values are applied only to print output; the image edit and soft proof are unchanged (the preview does not show them).
4. Save in the print template per paper: matte papers usually need more brightness lift than baryta.

## When to use instead
- Soft proof + a proof virtual copy for image-specific adjustments (local shadows, saturation for gamut).
- Print Adjustment is a global, per-paper calibration correction.

## Gotchas
- Large values (above +20) usually mean the display is too bright or the paper profile is wrong.
- Settings persist in Print Job panel for the next print; templates keep them explicit.

## Verify
- [ ] Shadow step wedge (zones I-III) separates on the print under viewing light; overall density matches the calibrated screen.
