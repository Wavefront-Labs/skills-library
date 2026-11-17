---
id: creative-arts.photography-fine-art.fine-art-printing.building-a-custom-printer-profile
name: building-a-custom-printer-profile
category: creative-arts
field: photography-fine-art
product: fine-art-printing
tags: [fine-art-printing, custom-printer-profile, profile-target-printing, spectrophotometer, profile-validation, i1profiler, adobe-color-printer-utility, delta-e]
level: practitioner
status: draft
description: "Build a custom ICC printer profile: print the target with colour management off, dry-down, measure with a spectrophotometer, generate and validate it."
sources: ["https://calibrite.com/ (i1Profiler / ColorChecker Studio)", "https://helpx.adobe.com/photoshop/kb/no-color-management-option-missing.html (Adobe Color Printer Utility)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building a custom printer profile

## Print the target
1. Generate the target in i1Profiler / ColorChecker Studio / ArgyllCMS (e.g. 1000-2000+ patches; more for
   wide gamut and for smooth B&W).
2. Print with **no colour management**: Photoshop can't disable colour management anymore - use **Adobe Color
   Printer Utility** (ACPU) or the profiling software's own print function.
3. Driver: media type and quality you will use with this profile; colour adjustment **Off (No Color Adjustment)**;
   record the settings exactly.
4. Let the target **dry-down 24 h** (minimum several hours) out of direct light.

## Measure
1. Spectrophotometer (i1Pro 3, ColorMunki/ ColorChecker Studio, i1iSis for automation) calibrated on its white tile.
2. Measurement mode: **M0** for OBA-free papers; **M1/M2** when OBAs present (M2 = UV-cut).
3. Scan rows on a backing board (same white backing used every time).
4. Generate the profile: choose gamut mapping, black generation defaults, and perceptual rendering options.

## Validate
1. Print a validation chart (or test image + IT8 subset) through the new profile with application-managed colour.
2. Measure and compare: average delta E2000 below about 1-2, max below about 4-5 is good.
3. Visual check of a neutral grey ramp (no colour tint), skin, saturated colours, shadow detail.

## Gotchas
- Profile is valid only for that printer, ink set, paper and driver settings.
- Printer drift: reprofile after ink changes or if prints shift.

## Verify
- [ ] Validation delta E within target and grey ramp neutral visually.
