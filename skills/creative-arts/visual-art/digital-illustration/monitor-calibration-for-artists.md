---
id: creative-arts.visual-art.digital-illustration.monitor-calibration-for-artists
name: monitor-calibration-for-artists
category: creative-arts
field: visual-art
product: digital-illustration
tags: [visual-art, digital-illustration, colour-management, monitor-calibration, colorimeter, displaycal, calibrite, d65, gamma-2-2, brightness-120, icc-profile]
level: practitioner
status: draft
description: "Calibrate and profile a monitor for painting and print matching: colorimeter, target white point and luminance, gamma, creating and loading the ICC profile, and recalibration schedule."
sources: ["https://displaycal.net/", "https://calibrite.com/", "https://docs.krita.org/en/general_concepts/colors/color_managed_workflow.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Monitor calibration for artists

**Goal:** a display that shows colours accurately and consistently, so digital art
looks right elsewhere and soft proofing means something (Krita Manual,
colour-managed workflow; DisplayCAL and colorimeter vendor guides).

## Hardware
- A **colorimeter** (Calibrite Display Plus/Pro, Datacolor Spyder). Built-in
  "calibration" by eye is not a substitute.
- Let the monitor warm up 30 minutes; set it to its native/sRGB or "custom" mode
  without dynamic contrast or eye-care modes.

## Targets
| Use | White point | Luminance | Gamma/tone curve |
|-----|-------------|-----------|------------------|
| General digital art / web | D65 (6500 K) | 100-140 cd/m2 | 2.2 or sRGB |
| Print matching in a dim room | D50-D65 (match your viewing light) | 80-120 cd/m2 | 2.2 |
- Lower luminance than factory settings (often 250-350 cd/m2) is the most
  important change for print work: prints look dark compared with a bright screen.

## Steps
1. Install software (vendor app or DisplayCAL with ArgyllCMS).
2. Set targets; follow prompts to adjust monitor brightness/RGB gains where possible.
3. Measure patches; the software creates an **ICC profile** and sets it as the
   system display profile (Windows Color Management; macOS Displays).
4. In Krita, Settings > Configure Krita > Colour Management: use the system monitor
   profile; in Photoshop it follows the OS.
5. **Verify** with the software's validation report (average delta E under 2 is good).

## Maintenance
Recalibrate every 4-8 weeks; after moving the monitor or changing settings.

## Gotchas
- Two monitors: profile each; never compare colour across an uncalibrated laptop.
- Wide-gamut monitor without colour-managed apps: oversaturated sRGB content.

## Verify
- [ ] Profile loaded at login, validation within tolerance.
- [ ] Luminance appropriate for print matching.
