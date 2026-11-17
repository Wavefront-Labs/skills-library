---
id: creative-arts.graphic-design.commercial-illustration.texture-and-grain-for-illustration
name: texture-and-grain-for-illustration
category: creative-arts
field: graphic-design
product: commercial-illustration
tags: [graphic-design, commercial-illustration, texture-brushes, grain, texture, noise, halftone-texture, vector-texture, procreate-brushes]
level: practitioner
status: draft
description: "Add texture and grain to vector and raster illustration: scanned textures, texture brushes, noise, halftone and masks, with resolution and print checks."
sources:
  - https://helpx.adobe.com/photoshop/user-guide.html
  - https://helpx.adobe.com/illustrator/user-guide.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Texture and grain for vector and raster

**Goal:** illustration that avoids a flat, digital look with texture that survives reproduction.

## Sources of texture
- **Scanned or photographed real marks:** paper, charcoal, ink spatter, gouache, sponge. Scan at 600 ppi or higher; use only textures you made or whose licence permits use.
- **Texture brushes:** brush sets in Photoshop, Procreate or Clip Studio; or build your own from a scanned mark (Photoshop: Edit > Define Brush Preset).
- **Procedural:** Photoshop **Filter > Noise > Add Noise** (Monochromatic checked, Gaussian), **Filter > Filter Gallery > Texture > Grain**; Illustrator offers raster effects under Effect (rasterised at the document raster effects resolution).

## Raster workflow (Photoshop)
1. Keep texture on its own layer above the art; set blend mode (**Multiply** for darkening texture, **Screen** or **Overlay** for light) and tune opacity.
2. Convert to grayscale and adjust Levels to a tight range for subtle grain.
3. Use a layer mask or clipping mask to apply texture only on selected shapes.
4. Add grain last, at final resolution, so it is not resampled; resampling or JPEG compression blurs it.

## Vector workflow (Illustrator)
- Use **Image Trace** on a high-contrast scan of a texture to get true vector speckles; keep node counts reasonable (large traces get heavy).
- Alternatively apply a raster texture as an **opacity mask** or a pattern swatch over vector shapes; this keeps shapes editable but makes the file mixed raster and vector.
- Brushes: scatter and art brushes with sampled marks give hand-drawn edge and speckle.
- Use **Effect > Document Raster Effects Settings** to set high enough resolution before printing.

## Print checks
- Fine grain can disappear or turn to mud on uncoated stock or with a small halftone dot; proof on the intended paper.
- Check CMYK conversion: textures at low contrast can vanish; ensure the texture does not create banding.
- For screen delivery, keep texture at 2x for high-density displays.

## Failure modes
- Texture applied at a different scale to the art; match its scale to mark size.
- Visible tiling; use a large source or randomise.
- Texture over text making it hard to read.
