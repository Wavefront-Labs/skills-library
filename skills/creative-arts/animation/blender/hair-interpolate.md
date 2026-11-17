---
id: creative-arts.animation.blender.hair-interpolate
name: hair-interpolate
category: creative-arts
field: animation
product: blender
tags: [blender, hair, hair-curves, hair-interpolate, interpolate-hair, duplicate-hair-curves]
level: practitioner
status: docs-checked
description: "Densify Blender Curves hair from guides with Interpolate Hair Curves and Duplicate Hair Curves: guides, distribution, masks, viewport amount and guide groups."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/hair/generation/interpolate_hair_curves.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/hair/generation/duplicate_hair_curves.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/hair/guides/create_guide_index_map.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# hair-interpolate

## Interpolate Hair Curves
Generates new curves by interpolating guide curves on a surface mesh. Inputs: **Resting Surface** (enable if Deform Curves on Surface comes after this node), **Follow Surface Normal**, **Part by Mesh Islands** (no blending across disconnected islands), **Interpolation Guides** (number of nearest guides used), **Distance to Guides**. Distribution: **Distribution Method** (Random or Poisson Disk), **Density**, **Density Mask** (scalar), **Mask Texture** (image sampled with the surface UV map), **Viewport Amount**, **Seed**. Outputs: Geometry, **Guide Index**, **Surface Normal**.

## Duplicate Hair Curves
Lighter alternative: copies each curve around itself within a radius. Inputs: **Amount**, **Viewport Amount**, **Radius**, **Distribution Shape**, **Tip Roundness**, **Even Thickness**, **Seed**. Outputs Geometry and Guide Index.

## Partings and groups
**Create Guide Index Map** takes Guides, Guide Distance, Guide Mask and **Group ID**: a curve only picks a guide with the same Group ID, so regions such as left and right sides do not mix. It writes guide_curve_index and outputs Guide Curves, Guide Index and Guide Selection.

## Practice
- Groom a small set of guides first (see hair-sculpt-mode), then interpolate.
- Use Viewport Amount to keep the viewport light; it does not change render density.
- Mask Texture is sampled after roots are generated, so it is not limited by mesh resolution; Density Mask is typically faster.

## Gotchas
- Interpolation needs the node to have a surface and UV map (via the Curves object's Surface settings or inputs).
- With Part by Mesh Islands off, guides can influence curves across separate parts.

## Verify
Render density looks even and no strands bridge across a parting or between islands.

## Checked

2026-10-27, Blender 5.2 manual (projects.blender.org blender-manual, branch blender-v5.2-release RST) and Python API docs. Compared every input and output with the Interpolate Hair Curves, Duplicate Hair Curves and Create Guide Index Map pages. Corrected: no Distance-to-Guides vertex-group mask (Density Mask and Mask Texture instead); Create Guide Index Map uses Group ID for partings. Removed guide and density counts, the duplicate-curves floating claim and the attachment dependency claim.
Method: documentation only; no commands were run.
