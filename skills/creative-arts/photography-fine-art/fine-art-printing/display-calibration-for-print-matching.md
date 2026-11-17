---
id: creative-arts.photography-fine-art.fine-art-printing.display-calibration-for-print-matching
name: display-calibration-for-print-matching
category: creative-arts
field: photography-fine-art
product: fine-art-printing
tags: [fine-art-printing, color-management, display-calibration, monitor-profiling, calibrite, displaycal, screen-to-print-match]
level: practitioner
status: draft
description: "Calibrate and profile a display for print matching: white point, luminance near 80-120 cd/m2, gamma, hardware puck, and verifying the profile."
sources: ["https://calibrite.com/", "https://displaycal.net/", "Jeff Schewe, The Digital Print (Peachpit)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Display calibration for print matching

The most common reason "prints come out too dark" is a display set far too bright.

## Targets (starting points)
- **White point**: D65 (6500 K) native for most displays; D50 matches a viewing booth more closely but often
  looks yellow on screen - many printers use D65 and judge prints under a D50 booth set to match brightness.
- **Luminance**: about 80-120 cd/m2 (dim room, prints compared under moderate light). Factory displays ship
  at 250-400 cd/m2.
- **Tone response**: gamma 2.2 (or sRGB curve); L* for some workflows.
- **Contrast**: native.

## Procedure
1. Warm up display 30 min; reset to factory/standard mode; disable dynamic contrast, eco modes, ambient sensors.
2. Use a colorimeter (Calibrite Display Plus HL / Pro HL, Datacolor Spyder) with Calibrite PROFILER or DisplayCAL.
3. Wide-gamut displays with hardware calibration (Eizo ColorNavigator, BenQ Palette Master): calibrate into the
   monitor's LUT - more accurate.
4. Save the ICC profile; the OS loads it.
5. Validate (DisplayCAL verification, average delta E under ~1-2).
6. Recalibrate monthly.

## Matching the print
Compare a print under your viewing light with the soft-proofed image; adjust **display luminance** (not the image)
until paper white on screen and in the booth look similar in brightness.

## Gotchas
- Laptop glossy displays and auto-brightness ruin matching.
- Mac "True Tone"/Night Shift must be off.

## Verify
- [ ] Profile validation passes; prints match soft proof in brightness under the booth.
