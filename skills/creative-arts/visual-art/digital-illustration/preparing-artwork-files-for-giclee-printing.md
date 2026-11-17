---
id: creative-arts.visual-art.digital-illustration.preparing-artwork-files-for-giclee-printing
name: preparing-artwork-files-for-giclee-printing
category: creative-arts
field: visual-art
product: digital-illustration
tags: [visual-art, digital-illustration, colour-management, color-management, giclee, print-prep, fine-art-print, tiff-export, print-resolution, bleed, soft-proofing, paper-profile]
level: practitioner
status: draft
description: "Prepare a digital artwork for giclee printing: pixel size at 300 ppi, colour space, flattening to TIFF, soft-proofing on the paper profile, bleed and borders, and test strips."
sources: ["https://helpx.adobe.com/photoshop/using/proofing-colors.html", "https://www.color.org/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Preparing artwork files for giclee printing

Giclee means archival inkjet printing (pigment inks, archival paper) - usually by a print studio. Your file decides most of the result.

## Resolution and size
- Ask the printer for their preferred resolution: usually **300 ppi at final print size** (240-360 acceptable). A 40 x 50 cm print at 300 ppi needs about 4724 x 5906 px.
- Paint at that size or larger from the start; upscaling a small canvas softens detail (AI upscalers can help but check artefacts).
- Keep the aspect ratio matching standard frame sizes if editions are sold framed.

## Colour
- Work in a wide-gamut RGB space (Adobe RGB or ProPhoto RGB in 16-bit) or sRGB if that's all your pipeline supports; **ask the printer** which they want - many prefer Adobe RGB, untagged files are a problem.
- Embed the ICC profile in the file.
- Do **not** convert to CMYK; inkjet printers are RGB devices driven by paper profiles.

## Soft proof
- Get the printer's **ICC profile for the printer + paper** combination (paper makers publish them, e.g. Hahnemuhle) or have them send it.
- Soft-proof (Photoshop: View > Proof Setup > Custom) with rendering intent (perceptual or relative colorimetric with black point compensation) and "simulate paper colour" on. Matte papers lose deep blacks and saturated colours - adjust on a duplicate or with adjustment layers for the print version.
- A calibrated monitor at a lower brightness (around 80-120 cd/m2) is needed for proofing to mean anything.

## File delivery
- Flatten a copy; save **TIFF** (LZW or no compression, 8-bit or 16-bit as requested). Keep the layered master separate.
- **Borders and bleed**: decide white border for signing (e.g. 2-5 cm) - either add it yourself or tell the printer. For edge-to-edge or canvas wraps add bleed/extra image (canvas wrap may need 4-5 cm extra each side or mirrored edges).
- Name files with title, size and paper: e.g. `title_40x50_photorag.tif`.

## Test strips
- Order a test strip or small proof on the actual paper before an edition; judge it under daylight-balanced light (around 5000 K).

## Gotchas
- Prints "too dark" usually come from an over-bright uncalibrated monitor.
- Missing ICC profile: printer guesses sRGB and colours shift.
- Saturated RGB blues/greens out of paper gamut flatten - check gamut warning.

## Verify
- [ ] 300 ppi at print size, profile embedded.
- [ ] Soft-proofed with the paper profile.
- [ ] Flattened TIFF plus border/bleed agreed; test strip approved.
