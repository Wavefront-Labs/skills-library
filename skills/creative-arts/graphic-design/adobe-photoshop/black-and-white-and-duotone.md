---
id: creative-arts.graphic-design.adobe-photoshop.black-and-white-and-duotone
name: black-and-white-and-duotone
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, adjustment-layers, tonal-correction, black-and-white-conversion, duotone, gradient-map, spot-colour-duotone, monochrome, two-colour-print]
level: practitioner
status: draft
description: "Convert to black and white with control and make duotones: gradient-map duotones for screen and true spot-colour duotones for two-colour print."
sources:
  - https://helpx.adobe.com/photoshop/using/convert-color-image-black-white.html
  - https://helpx.adobe.com/photoshop/using/duotones.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Black and white conversion and duotones

**Goal:** strong monochrome images with intentional tonal separation, and duotones that print correctly.

## Black and white
- **Black & White adjustment layer** (not Image > Mode > Grayscale, which throws away control).
  Sliders set how bright each original colour becomes: darken Blues for dramatic skies, lighten
  Reds/Yellows for skin. Targeted tool: click-drag on an area to change its source colour's brightness.
- Add Curves above for contrast; Tint checkbox for a simple toned image.
- Alternative: Channel Mixer with **Monochrome**, keeping R+G+B near 100%.
- Convert the mode to Grayscale at the end only if the deliverable must be a single-channel
  grey file (e.g. 1-colour newspaper print).

## Duotone for screen (and CMYK print)
**Gradient Map adjustment layer**: shadows colour -> highlights colour (e.g. navy to pink). Add
a midpoint stop for tritones. Set Dither on. Easy, editable, any palette - the "Spotify duotone" look.

## True duotone for spot-colour print
For jobs printing with, say, black + one Pantone:
1. Convert to Grayscale (after a Black & White adjustment and flatten on a copy).
2. Image > Mode > **Duotone**. Type: Duotone (or Monotone/Tritone/Quadtone).
3. Ink 1: Black; Ink 2: click the colour box > Color Libraries > choose the Pantone. **Names must
   match** the swatch used in InDesign exactly.
4. Click each ink's **curve** to control where it appears (e.g. Pantone in midtones/highlights,
   black limited in highlights). Use the presets as a starting point.
5. Save as **Photoshop PSD or EPS/PDF** (Duotone mode is preserved). Place in InDesign and check
   Separations Preview shows exactly the two plates.

## Gotchas
- Duotone mode files cannot be layered with adjustment layers in the usual way; keep the RGB master.
- Gradient-map duotones in a CMYK job become 4-colour builds, not spot colours.
- Overprint preview needed to see a real duotone's appearance in InDesign/Acrobat.

## Verify
- [ ] Monochrome images have deliberate tonal separation (sky vs subject) and no blocked shadows.
- [ ] Spot duotones: Separations Preview shows only the intended inks, names identical to layout swatches.
