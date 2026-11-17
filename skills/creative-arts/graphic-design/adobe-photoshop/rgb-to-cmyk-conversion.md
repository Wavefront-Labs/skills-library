---
id: creative-arts.graphic-design.adobe-photoshop.rgb-to-cmyk-conversion
name: rgb-to-cmyk-conversion
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-color-management, color-modes, rgb-to-cmyk, rendering-intent, convert-to-profile, relative-colorimetric, perceptual, black-point-compensation, total-ink-limit, gcr]
level: advanced
status: draft
description: "Convert RGB images to CMYK in Photoshop properly: when to convert at all, the printer's profile, perceptual vs relative colorimetric, and ink totals."
sources:
  - https://helpx.adobe.com/photoshop/using/converting-color-modes.html
  - https://helpx.adobe.com/photoshop/using/color-settings.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RGB to CMYK conversion

**Goal:** CMYK images that print as close to the RGB original as the press allows, converted once, with the right profile.

## Should you convert at all?
- **PDF/X-4 workflow:** keep images RGB with embedded profiles; InDesign/the RIP converts to the
  output intent at export/print. Simpler, repurposable, often better.
- **Convert in Photoshop** when the printer demands CMYK files, when you need to fine-tune
  out-of-gamut colours by hand, or when delivering to PDF/X-1a (CMYK only).
- Keep the **RGB master**; CMYK is a delivery copy.

## Convert (Edit > Convert to Profile)
1. Destination Space: the **printer's profile** (e.g. PSO Coated v3, Coated FOGRA39, GRACoL2013,
   or an uncoated profile). Not the generic "CMYK" mode setting unless the working space is already right.
2. Engine: Adobe (ACE). **Intent:**
   - **Relative Colorimetric** + **Black Point Compensation**: keeps in-gamut colours accurate, clips
     out-of-gamut ones to the nearest printable colour. Good default for most images and brand-critical colours.
   - **Perceptual**: compresses the whole gamut to keep relationships between colours; better for
     very saturated images with lots of out-of-gamut colour (neon, saturated product shots).
   Compare both with Preview on, viewing problem areas.
3. Flatten option if delivering flat; otherwise keep layers (adjustment layers are recalculated in CMYK).

Image > Mode > CMYK uses the working CMYK space from Color Settings - same result if that matches the printer.

## After conversion
- Check **total area coverage**: Info panel set to show Total Ink; darkest areas should be under the
  profile's limit (~300-330% coated, ~260-300% uncoated). The profile's GCR/UCR settings handle this
  if you used the right profile.
- Neutral greys may not have equal CMY - that is normal.
- Do not convert back to RGB and again to CMYK - each round trip loses gamut.

## Gotchas
- Bright RGB greens, blues and oranges dull noticeably - warn clients early; consider spot colours for brand colours.
- Pure RGB black (0,0,0) converts to a rich 4-colour black - fine for images, wrong for small text (keep text in layout as 100K).
- Converting with the wrong profile (coated for uncoated paper) = too much ink, muddy shadows.

## Verify
- [ ] Converted with the printer's named profile; profile embedded in the saved file.
- [ ] Total ink below the limit in the darkest areas.
- [ ] RGB master kept.
