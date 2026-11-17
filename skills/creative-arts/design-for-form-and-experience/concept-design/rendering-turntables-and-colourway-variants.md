---
id: creative-arts.design-for-form-and-experience.concept-design.rendering-turntables-and-colourway-variants
name: rendering-turntables-and-colourway-variants
category: creative-arts
field: design-for-form-and-experience
product: concept-design
tags: [turntable-render, colorway-renders, colourway, product-rendering, animation-render, variant-rendering]
level: practitioner
status: draft
description: "Produce turntable animations and colourway renders: camera setup, frame count, loop closure, and consistent variants from one master scene."
sources:
  - "Koos Eissen and Roselien Steur, Product Design Rendering (BIS Publishers)"
  - "IDSA (idsa.org) education resources"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Turntables and colourway renders

## Turntable
1. Fix the camera at the hero angle; a moderate focal length (about 50-85 mm equivalent) limits distortion on small products.
2. Rotate the **product on a pivot at its centre** (or rotate the environment) through 360 degrees.
3. **Frames:** at 24 fps, 5 s is 120 frames. The last frame must not duplicate the first: render frames 0 to N-1 so it loops.
4. Use **linear interpolation** on the rotation, not ease in and out, so the loop does not slow at the seam.
5. Lock exposure and denoise settings; render a still at final resolution first, then test noise on a moving frame.
6. Render a PNG sequence (not compressed video) and compile with ffmpeg or an editor to H.264 MP4 or whatever the platform needs.

## Colourways
1. Build **one master scene** with materials grouped by CMF role (body, accent, trim).
2. Use **material variants or scene states** to switch colours; do not duplicate files.
3. Lock camera, lighting and framing; only materials change.
4. Name outputs consistently: product_colourway_view_v01.png.
5. Lay out a **colourway grid** at one scale with CMF names and codes (see `...concept-design.building-a-cmf-strategy-for-a-product-line`).

## Verify
- [ ] The loop does not hitch at the seam.
- [ ] Variants differ only in materials.
- [ ] Colour names match the CMF codes.
