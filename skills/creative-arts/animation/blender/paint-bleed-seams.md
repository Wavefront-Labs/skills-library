---
id: creative-arts.animation.blender.paint-bleed-seams
name: paint-bleed-seams
category: creative-arts
field: animation
product: blender
tags: [blender, texture-paint, paint-bleed, seam-bleed, dilate-paint, uv-seams, occlude, backface-culling]
level: practitioner
status: docs-checked
description: "Reduce visible UV seams when texture painting in Blender: Bleed (seam bleed), Occlude, Backface Culling, Dither, painting across seams in 3D and cloning over leftovers."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/texture_paint/tool_settings/options.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# paint-bleed-seams

Goal: seams that are invisible in render and survive texture filtering.

## Options panel (Texture Paint tool settings > Options)
- **Bleed**: Seam Bleed extends the paint beyond UV island bounds to avoid visual artefacts (like the bake margin). Raise it for large or mipmapped maps (practice).
- **Dither**: amount of dithering when painting on 8-bit images.
- **Occlude**: with geometry occlusion active only exposed pixels (not hidden by other mesh parts) are affected; this also allows 3D stencils to mask out areas of the surface.
- **Backface Culling**: only the front side of faces can be painted.

## Workflow (practice)
1. Paint in the 3D Viewport rather than the Image Editor: projection painting continues a stroke across islands, so seams match.
2. Paint over seams from a view facing both sides, with a second pass from another angle to fill gaps.
3. For leftover lines use a Clone or Smear brush across the seam in 3D.
4. Check results in the Image Editor: islands should have painted margin around them.

## Gotchas
- Bleed can only extend into empty texture space, so tightly packed islands cannot bleed (practice); re-pack with more margin before painting.
- The 2D Image Editor only knows UV space, so strokes there do not cross seams (practice).
- Overlapping or mirrored UVs paint both sides at once; that is not a seam bug (practice).

## Verify
Orbit close to seams in Material Preview; no visible line should remain.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release) sculpt_paint/texture_paint/tool_settings/options.rst (Bleed, Dither, Occlude, Backface Culling wording). Removed: Bleed default of 2 px and the 8-16 px advice, the Normal angle falloff option (not in the Options panel), the Cycles bake dilate step and margin figures, UV margin number, and the Preferences mipmapping path. The workflow items are practice. Method: documentation only; no commands were run.
