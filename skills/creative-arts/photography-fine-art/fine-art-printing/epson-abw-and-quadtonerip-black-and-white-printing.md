---
id: creative-arts.photography-fine-art.fine-art-printing.epson-abw-and-quadtonerip-black-and-white-printing
name: epson-abw-and-quadtonerip-black-and-white-printing
category: creative-arts
field: photography-fine-art
product: fine-art-printing
tags: [fine-art-printing, black-and-white-inkjet, advanced-black-and-white, quadtonerip, abw-mode, toned-bw-print, piezography]
level: practitioner
status: draft
description: "Print neutral or toned black-and-white inkjet prints with Epson Advanced B&W mode or QuadToneRIP, including toning, linearisation and settings."
sources: ["https://epson.com/ (Advanced Black and White Photo mode guide)", "https://www.quadtonerip.com/", "https://www.piezography.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Epson ABW and QuadToneRIP black-and-white printing

## Epson Advanced Black and White Photo (ABW)
- Uses mostly the black and grey inks with small colour ink amounts for neutrality.
1. Image in greyscale or RGB (neutral). Application: **Printer Manages Colors** (or "no colour management"
   with ABW - Lightroom: Profile = Managed by Printer).
2. Driver: Color = **Advanced B&W Photo**; media type as for your paper.
3. Advanced/Color Controls: Color Toning (Neutral, Cool, Warmish, Warm, Sepia) or custom tint via the colour
   circle; Tone (Darker, Dark, Normal, Light); Shadow/Highlight Tonality; Max Optical Density; Highlight Point Shift.
4. Make a test strip of tone settings; save a preset.
- No ICC soft proof is available for ABW; build a reference print and judge by eye (or make a custom ABW profile with grey targets).

## QuadToneRIP (Roy Harrington)
- A shareware RIP for Epson printers that drives each ink channel through paper-specific curves - very smooth
  and fine control of toning and density.
1. Install QTR and the curve set for your printer model; choose a curve for your paper (or build one with
   QTR's linearisation tools, measuring a step wedge).
2. Print via the QTR print tool (Windows) or as a printer/PPD (macOS).
3. Mix warm/cool curves for split-toned blacks (e.g. warm highlights, neutral shadows).

## Piezography
Dedicated carbon/grey ink sets (Piezography, Jon Cone) replace the colour inks - highest neutrality and
permanence; needs a dedicated printer and QTR/Piezography software.

## Verify
- [ ] Grey step wedge smooth and neutral (or intended tone) under display light.
