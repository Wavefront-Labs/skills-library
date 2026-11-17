---
id: creative-arts.visual-art.digital-illustration.colour-profiles-and-soft-proofing
name: colour-profiles-and-soft-proofing
category: creative-arts
field: visual-art
product: digital-illustration
tags: [visual-art, digital-illustration, colour-management, color-management, soft-proofing, icc-profile, srgb, adobe-rgb, cmyk, rendering-intent, krita, photoshop, gamut-warning]
level: practitioner
status: draft
description: "Manage colour in digital art: choosing a working space (sRGB vs Adobe RGB), embedding ICC profiles, soft proofing to a printer or CMYK profile with gamut warnings, and rendering intents."
sources: ["https://docs.krita.org/en/general_concepts/colors/color_managed_workflow.html", "https://helpx.adobe.com/photoshop/using/proofing-colors.html", "https://www.color.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Colour profiles and soft proofing

**Goal:** colours that look as intended on other screens and in print (Krita
Manual, colour managed workflow; Adobe proofing docs; ICC).

## Working space
- **sRGB**: default for web and most screens; safest for online work.
- **Adobe RGB / Display P3**: wider gamut, useful if printing on wide-gamut printers
  or for Apple displays; colours outside sRGB will shift when posted online.
- Choose at document creation; converting later is possible (Image > Convert colour
  space), not "assign" (which reinterprets numbers).
- **Embed the profile** when saving/exporting.

## Soft proofing
1. Get the ICC profile for the printer + paper combination (print labs provide
   them) or a standard CMYK profile (e.g. FOGRA39/ISO Coated v2 in Europe, GRACoL/SWOP
   in the US) for press.
2. Krita: View > Soft Proofing (Ctrl+Y) with the profile set in Image > Image
   Properties > Soft proofing; enable gamut warning. Photoshop: View > Proof Setup >
   Custom, then View > Proof Colors (Ctrl+Y) and Gamut Warning.
3. Choose a **rendering intent**: *Perceptual* compresses the whole gamut smoothly
   (photographic, painterly work); *Relative colorimetric* keeps in-gamut colours
   exact and clips out-of-gamut ones (with black point compensation).
4. Adjust out-of-gamut saturated colours (bright blues, greens, oranges) while proofing
   so they degrade gracefully.

## Paint in RGB, convert at the end
Painting in CMYK limits tools and blending; most illustrators paint in RGB and
convert or let the lab convert, after proofing.

## Gotchas
- Uncalibrated monitor: proofing is meaningless (see monitor calibration).
- Exporting without an embedded profile: browsers and labs guess.
- Paper white simulation makes proofs look duller; that is the point.

## Verify
- [ ] Working space chosen deliberately and embedded.
- [ ] Soft proof checked with the actual print profile.
- [ ] Out-of-gamut colours adjusted.
