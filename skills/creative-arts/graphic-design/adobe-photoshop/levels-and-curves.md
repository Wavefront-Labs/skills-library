---
id: creative-arts.graphic-design.adobe-photoshop.levels-and-curves
name: levels-and-curves
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, adjustment-layers, tonal-correction, levels-adjustment, curves-adjustment, histogram, black-point, white-point, s-curve, clipping, info-panel]
level: practitioner
status: draft
description: "Correct tone with Levels and Curves adjustment layers: read the histogram, set black and white points without clipping, S-curves and targeted edits."
sources:
  - https://helpx.adobe.com/photoshop/using/levels-adjustment.html
  - https://helpx.adobe.com/photoshop/using/curves-adjustment.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Levels and Curves

**Goal:** a full tonal range with controlled contrast, done on adjustment layers so it can be revised.

## Read the histogram first
Window > Histogram (or in the Levels dialog). Gaps at the ends = image does not reach black or
white (flat). A spike jammed against an end = clipping (lost detail). Mountain mostly left =
dark (low key), right = bright.

## Levels (adjustment layer)
1. Drag the **black input** slider to where the histogram starts and the **white input** to where
   it ends. **Alt/Option+drag** shows clipping: stop just before significant areas turn
   solid white/black (specular highlights may clip).
2. **Midtone (gamma)** slider brightens or darkens midtones without moving ends.
3. Output sliders reduce range (e.g. limit to 5-250 for print or for a faded look).
4. Auto (with Options: "Find Dark & Light Colors", "Snap Neutral Midtones") is a decent start.

## Curves (adjustment layer)
- Diagonal line = no change. Drag up = brighter, down = darker, at that tone.
- **S-curve:** pull the upper third up and lower third down - more contrast in midtones.
  Inverse S reduces contrast.
- **Targeted adjustment tool** (hand icon): click-drag on the image area you want to change.
- Set **black and white points** with the eyedroppers on the darkest/lightest real detail
  (Alt/Option+drag end points also shows clipping).
- Per-channel curves (Red/Green/Blue) fix colour casts (see colour cast skill).
- Set the layer to **Luminosity** blend mode so contrast changes do not shift saturation.

## Professional habits
- Use Info panel colour samplers (Shift+click with eyedropper) to watch numbers on key areas
  (skin, neutrals, highlights) while adjusting.
- Mask the adjustment for local correction (darken a sky, lift a face).
- Several gentle curves beat one extreme one; group them as "Tone".

## Gotchas
- Strong curves in 8-bit cause banding/posterisation in skies; work in 16-bit for heavy edits.
- Print darkens images (dot gain); judge with soft proofing, not only on a bright screen.

## Verify
- [ ] Histogram spans the range without important clipping.
- [ ] Highlights hold detail (e.g. RGB < 250 on white fabric) and shadows are not blocked.
- [ ] Corrections live on adjustment layers.
