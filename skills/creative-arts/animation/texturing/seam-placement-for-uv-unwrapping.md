---
id: creative-arts.animation.texturing.seam-placement-for-uv-unwrapping
name: seam-placement-for-uv-unwrapping
category: creative-arts
field: animation
product: texturing
tags: [seam-placement, uv-seams, uv-layout, unwrapping, hard-edges, stretching, unwrap]
level: practitioner
status: draft
description: "Place UV seams to minimise stretching and visible texture breaks: hidden locations, hard-edge alignment for normal maps, per-shape cut strategies and verification."
sources:
  - https://www.blender.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Seam placement

A **seam** is an edge cut so the 3D surface can be flattened to 2D. Good seams are as few as possible, where they will be hard to see, and positioned to give low distortion.

## Where to put them
1. **Hidden areas**: underneath, behind, inside, along natural garment lines, under hair, at the back of the head, at the rim of an object that meets the ground.
2. **Natural borders**: material changes, panel lines, and creases where a texture break looks intentional.
3. **Hard edges**: align seams with hard (split) edges. Normal maps are baked per smoothing group; a seam on a hard edge reduces visible shading discontinuities (`normal-map-directx-opengl.md`).
4. **Cylinders and limbs**: a single seam along the length, on the least-visible side; caps get their own islands.
5. **Spheres and heads**: avoid pole stretching with a sensible cut (like a peeled orange or a vertical seam from the back), and choose the seam to follow the hairline or ear.
6. **Symmetry**: cut along the middle plane for mirrored objects and mirror or overlap halves when the texture allows it.

## Minimise distortion
- More seams give less stretching but more visible breaks and wasted space; balance them.
- Straighten islands (rectangular parts, panels) so they pack well and texture lines stay straight.
- Check stretching with a **checker texture**: squares should look square and about the same size everywhere.

## Blender notes
- Select edges, then Edge > Mark Seam (Ctrl+E menu in Edit Mode) and Unwrap (U); methods include Angle Based and Conformal. Smart UV Project is automatic and handy for rough work but gives many islands.
- Use the UV Editor's Stretch display to see distortion.

## Gotchas
- Seams on the visible front of a hero asset show when the texture has strong low-frequency detail; hand-paint across seams in Painter only if the projection supports it.
- Do not leave a seam in the middle of a flat visible surface.

## Verify
- [ ] Checker shows even squares across the model.
- [ ] Seams are hidden or aligned to hard edges.
- [ ] Seam count is as low as the shape allows.
