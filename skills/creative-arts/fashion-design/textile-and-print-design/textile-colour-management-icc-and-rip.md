---
id: creative-arts.fashion-design.textile-and-print-design.textile-colour-management-icc-and-rip
name: textile-colour-management-icc-and-rip
category: creative-arts
field: fashion-design
product: textile-and-print-design
tags: [fashion-design, textile-and-print-design, textile-icc-profile, rip-software, colour-management, digital-textile-printing, print-design]
level: practitioner
status: draft
description: "Manage colour for digital textile printing: fabric-specific ICC profiles, RIP software, colour libraries, soft proofing, spot colour matching and strike-off loops."
sources:
  - https://en.wikipedia.org/wiki/ICC_profile
  - https://en.wikipedia.org/wiki/Raster_image_processor
  - https://en.wikipedia.org/wiki/Digital_textile_printing
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Textile colour management, ICC profiles and RIP

**Goal:** colours on fabric that match the approved standard, repeatably, across runs and mills.

## The chain
Design file (RGB/Lab/spot) -> RIP (raster image processor: e.g. Caldera, ErgoSoft, Inèdit
NeoStampa, Wasatch) -> printer with ink set -> fabric -> fixation (steam/heat) -> wash.
Each step changes colour; the **ICC profile** describes one specific combination of printer,
ink, fabric, pretreatment and fixation.

## Practice
1. Use a profile built for the exact fabric and process; a cotton reactive profile on silk is wrong.
2. Send files in a defined space (Adobe RGB, sRGB or Lab) and state it; or use spot colours
   named from a library (Pantone TCX/TPG or the printer's colour book).
3. For brand colours, print a **colour book / patch chart** from the RIP on the target fabric and
   pick the nearest patch; specify by patch number.
4. Soft proof on a calibrated monitor (hardware calibrated, D50/D65 per workflow) only as a guide.
5. Approve with a physical strike-off under standard light (D65 lightbox), and measure with
   a spectrophotometer: Delta E (CMC 2:1) under ~1.0-1.5 is a common tolerance.

## Gotchas
- Out-of-gamut colours (neon, some turquoises, deep reds on polyester) cannot be reached; agree
  the nearest or change process.
- Metamerism: a match in daylight may fail under shop lighting; check D65 and TL84/LED.
- Re-running months later on a new fabric lot shifts colour; keep the approved strike-off.

## Verify
- [ ] Profile matches fabric and ink.
- [ ] Spot colours named and approved by strike-off.
- [ ] Delta E and light sources recorded.
