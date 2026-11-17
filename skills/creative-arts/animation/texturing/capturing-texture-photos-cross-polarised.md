---
id: creative-arts.animation.texturing.capturing-texture-photos-cross-polarised
name: capturing-texture-photos-cross-polarised
category: creative-arts
field: animation
product: texturing
tags: [texture-capture, cross-polarised, polarised-photography, photogrammetry, albedo-capture, colour-checker, texturing]
level: advanced
status: draft
description: "Photograph surfaces for albedo with cross-polarised light: filter setup, camera settings, colour checker, shooting pattern, and what to check before leaving the site."
sources:
  - https://helpx.adobe.com/substance-3d-painter
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Capturing texture photos (cross-polarised)

Cross-polarisation removes specular reflection from a photograph, leaving diffuse colour for use as albedo. It needs a **polarising filter on the lens** and **polarised light** (linear polarising film on the lights, or a polarised flash).

## Principle
Light reflecting from a glossy surface keeps its polarisation, while light that scatters inside the surface becomes unpolarised. If the light is polarised one way and the lens filter is rotated 90 degrees to it, the specular part is blocked and the diffuse part passes.

## Kit
- Camera with RAW, tripod, remote release.
- Circular polariser for the lens, plus linear polarising film over each light (or a ring light with a polariser).
- Colour checker or grey card, and a scale reference.
- Diffuse, even lighting (two lights at a low angle on each side, or a flash), or shade and overcast sky when shooting outdoors.

## Procedure
1. Set up lights evenly and place the polarising film in front, with orientation marked.
2. Mount the polariser on the lens and **rotate it while watching a live view of a shiny part of the surface** until highlights are at their minimum.
3. Set manual exposure and white balance. Use low ISO, an aperture around f/8 to f/11 for sharpness and depth, and a shutter speed that suits the light; avoid auto exposure.
4. Include the **colour checker** in the first frame (and once per light set-up) to calibrate colour in the raw converter.
5. Shoot square-on, with the camera plane parallel to the surface; use enough overlap for photogrammetry (commonly 60-80%) when you will reconstruct geometry.
6. Shoot a second set without polarisation if you also want to separate specular detail for roughness reference.
7. Review in the field: zoom in on a test frame for focus, clipping and residual reflections.

## Processing
- Develop RAW with the checker-derived white balance and consistent settings; export to linear or the working space (`acescg-working-space.md` for ACES pipelines).
- Remove remaining shading (`delighting-source-photos.md`) and make tileable if needed (`seamless-tiling-textures.md`).

## Gotchas
- Metals reflect differently: polarisation does not fully remove their reflections.
- Mismatched polariser rotation lets highlights return; re-check if lights move.
- Fading daylight changes between frames; cross-polarisation under artificial light is more repeatable.

## Verify
- [ ] Highlights suppressed on test frames.
- [ ] Colour checker in frame; settings fixed.
