---
id: creative-arts.animation.blender.remesh-modifier-modes
name: remesh-modifier-modes
category: creative-arts
field: animation
product: blender
tags: [blender, remesh, modifiers, voxel, octree, blocks, smooth, sharp]
level: practitioner
status: verified
description: "Regenerate clean quad topology with Blender's Remesh modifier: Blocks, Smooth, Sharp and Voxel modes, Octree Depth, Scale, Remove Disconnected and what each setting does."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/remesh.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# remesh-modifier-modes

Goal: generate new topology that follows the input surface, for sculpt bases or merging overlapping parts. Output contains only quads in the octree modes.

## Modes

The three octree modes give almost identical topology; they differ in smoothing.
- **Blocks**: no smoothing.
- **Smooth**: smooth surface.
- **Sharp**: like Smooth but preserves sharp edges and corners. **Sharpness**: higher values give edges closer to the input, lower values filter out noise.
- **Voxel**: uses OpenVDB to generate a new manifold mesh while trying to preserve the original volume. **Adaptivity** reduces face count where detail is not needed and introduces triangulation. **Smooth Shading** outputs smooth-shaded faces.

## Common settings (octree modes)

- **Octree Depth**: resolution of the output; low values give larger faces, high values denser output.
- **Scale**: lower values effectively decrease output resolution.
- **Remove Disconnected** + **Threshold**: removes small isolated pieces (thin input parts can become loose); Threshold controls how small a component must be to be removed.
- **Smooth Shading**: smooth rather than flat shading; the input's shading is not preserved.

## Notes

- The input mesh should have some thickness; for a completely flat input add a Solidify modifier above Remesh.
- Voxel mode has a Voxel Size setting (default 0.1; on a 2-unit cube 0.1 gave 2,646 faces and 0.05 gave 10,086), which the 5.2 manual page does not describe.

## Verify

Compare face count and shape before and after, and check for stray floating pieces.

## Checked

Date: 2026-10-27. Documentation release: Blender manual, 5.2 release branch (Remesh modifier page). Confirmed: mode names and behaviours, Sharpness, Adaptivity, Octree Depth, Scale, Remove Disconnected, Threshold, thickness note. Removed unconfirmed voxel-size figures, doubling rules, recipes, UV/attribute and performance claims.

Run check, 2026-11-01, Blender 4.5.14 LTS headless: Remesh with Python on a cube: modes Blocks, Smooth, Sharp and Voxel (default Voxel; Octree Depth 4, Scale 0.9, Sharpness 1.0, Threshold 1.0, Adaptivity 0); the three octree modes gave the same 1,350 quads (all faces 4-sided), differing only in position (Blocks extent 1.042, Smooth and Sharp 1.0); Octree Depth 2, 4 and 6 gave 54, 1,350 and 19,494 faces; Scale 0.5 gave 384 faces, 0.9 and 1.0 gave 1,350; Smooth Shading toggled flat and smooth faces; Voxel gave quads and Adaptivity 0.5 added triangles; Remove Disconnected with Threshold 1.0 removed a tiny separate cube (528 to 522 faces) while Threshold 0 kept it; a flat plane gave 0 faces and worked with Solidify above Remesh (510 faces). Not run: the mode smoothing differences beyond extents and UV/attribute behaviour.

Method: manual text confirmed from documentation; behaviour run headless in Blender 4.5.14.
