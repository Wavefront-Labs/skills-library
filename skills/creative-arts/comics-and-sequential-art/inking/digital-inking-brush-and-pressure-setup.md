---
id: creative-arts.comics-and-sequential-art.inking.digital-inking-brush-and-pressure-setup
name: digital-inking-brush-and-pressure-setup
category: creative-arts
field: comics-and-sequential-art
product: inking
tags: [inking, digital-inking, inking-brush-settings, pressure-curve, clip-studio-paint, csp-brushes, csp-pen-pressure, photoshop, procreate, antialiasing, pen-tablet]
level: practitioner
status: draft
description: "Set up digital inking brushes: pressure-to-size curves, minimum size, anti-aliasing for print vs screen, canvas resolution, and calibrating tablet pressure so lines taper like a brush."
sources:
  - https://help.clip-studio.com/en-us/First_Topic.htm
  - https://helpx.adobe.com/photoshop/using/brush-settings.html
  - https://openlibrary.org/search?q=Art+of+Comic+Book+Inking
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Digital inking brush and pressure setup

**Goal:** digital strokes with the taper and control of a good brush or nib.

## Canvas first
- Ink at print size at **600 dpi** (common for line art; some use 1200 for bitmap
  output), or at original-art size at a matching resolution. Low-res canvases make
  even good brushes look soft.

## Brush settings that matter (names from Clip Studio Paint / Photoshop)
| Setting | Recommendation |
|---|---|
| Size affected by pressure | ON |
| Minimum size | ~5-20% of max for taper; 0% gives hair-thin ends that may drop out in print |
| Opacity affected by pressure | OFF for inks (solid black lines) |
| Anti-aliasing | for print bitmap: none/weak; for colour/screen: medium |
| Hardness | 100% (no soft edges) |
| Spacing | low (~5-10% in Photoshop) for smooth strokes |
| Colour | pure black (RGB 0,0,0 / K100) |

## Pressure curve
1. In the app (CSP: File/Preferences > Tablet > Adjust pen pressure settings; or the
   brush's pressure graph), draw several strokes from light to heavy so it calibrates.
2. If thin lines need too much effort: lift the curve (softer); if lines go thick too
   easily: flatten it (firmer).
3. Also check the tablet driver's own pressure setting; set one, keep the other neutral
   to avoid double curves.

## Tool choice
- G-pen style (sharp taper, crisp) for figures.
- Mapping/maru-style (fine, little variation) for detail and backgrounds.
- Round brush with texture for organic work.
- Save a small set of named custom brushes; consistency across pages matters.

## Gotchas
- Anti-aliased lines converted to bitmap get jaggy or broken; ink without
  anti-aliasing if bitmap output is required.
- Zooming changes perceived line weight; check at print size (100% at physical size).

## Verify
- [ ] Test sheet: thin-to-thick strokes taper smoothly.
- [ ] Lines solid black, no grey anti-alias where bitmap output is needed.
