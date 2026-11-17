---
id: creative-arts.comics-and-sequential-art.clip-studio-paint.tone-layers-and-tone-area-display-in-csp
name: tone-layers-and-tone-area-display-in-csp
category: creative-arts
field: comics-and-sequential-art
product: clip-studio-paint
tags: [clip-studio-paint, csp-tones, csp-tone-layer, tone-area, screentone, layer-property-tone, frequency-lpi]
level: practitioner
status: draft
description: "Create and manage tone layers in Clip Studio Paint: new tone from a selection, frequency and dot settings, tone area display, editing the tone area and checking monochrome output."
sources:
  - https://tips.clip-studio.com/en-us
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tone layers and tone areas

## Create a tone layer
1. Select the area (Auto select with "refer other layers", or lasso).
2. Selection launcher > **New tone**, or Layer > New layer > **Tone**.
3. Dialog: **Frequency** (lines per inch, e.g. 50-65 lpi for print manga at 600 dpi), **Density** (%),
   **Type** (circle/dot, line, noise, cross, etc.), **Angle** (45 degrees default), position.
4. A tone layer is a fill layer with a layer mask; the mask is the tone area.

## Edit the tone area
- Paint on the mask with a pen to add tone, erase to remove (or use transparency colour).
- **View > Tone area** highlights all tone areas in a colour, making gaps and overflow visible.
- Layer property palette > **Tone** effect settings change frequency/dot type later without redrawing.

## Greyscale to tone
- Paint in grey on a normal layer, then set Layer property > Effect > **Tone**. Grey values become dot
  sizes. Use "Use image color" or "Use layer color" as needed.

## Output
- Comic pages for print: page expression colour Monochrome, tones as dots at 600 dpi; export with
  "Monochrome 2-tone" to get pure bitmap dots.
- Preview at 100% (Actual pixels) to judge moire; on-screen zooms show false moire.

## Gotchas
- Stacking two dot tones at the same angle and different lpi moires; keep consistent frequency per
  page.
- Scaling a raster tone layer after conversion blurs dots; keep the effect live until export.

## Verify
- [ ] Tone area display shows no gaps along line art.
- [ ] Monochrome 2-tone export shows clean dots.
