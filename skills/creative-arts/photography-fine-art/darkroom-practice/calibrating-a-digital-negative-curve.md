---
id: creative-arts.photography-fine-art.darkroom-practice.calibrating-a-digital-negative-curve
name: calibrating-a-digital-negative-curve
category: creative-arts
field: photography-fine-art
product: darkroom-practice
tags: [darkroom-practice, digital-negatives, digital-negative-curve, easy-digital-negatives, pictorico, step-wedge-calibration, chartthrob, linearization]
level: practitioner
status: draft
description: "Make digital negatives for contact processes: inkjet transparency, step-wedge printing, measuring the process response, and building a linearising curve."
sources: ["Peter Mrhar, Digital Negatives (Easy Digital Negatives method)", "https://www.easydigitalnegatives.com/", "Ron Reeder, Digital Negatives with Epson Printers"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Calibrating a digital negative curve

## Materials
Inkjet transparency film (Pictorico OHP Premium, Fixxons), pigment printer, step wedge file (21 or 101
steps), the alternative process paper/chemistry you will print with.

## Procedure
1. **Standard printing time (SPT)**: print a solid black (or the max-density colour) negative patch,
   then make an exposure test on the alt process - SPT is the shortest time giving maximum black through
   that patch.
2. **Colour blocker** (for UV processes): find an ink colour (e.g. a specific green/orange) that blocks UV
   well; some methods print negatives in a colour rather than black (Easy Digital Negatives).
3. **Print the step wedge** as a negative with no curve (printer colour management off or fixed settings).
4. Contact print the wedge at SPT; process normally; dry.
5. Scan or measure the print (densitometer/scanner) for each step.
6. Build the correction curve (Photoshop curves; ChartThrob; EDN or Precision Digital Negatives tools):
   it maps input values so the printed result is linear.
7. Apply the curve to future images (invert, flip if required, apply curve), print, and verify with a
   second wedge; iterate 2-3 times.

## Gotchas
- Printer settings must be identical each time (media type, resolution, colour mode).
- Humidity changes alt-process response - recheck seasonally.

## Verify
- [ ] Verification wedge prints with even steps from paper white to Dmax.
