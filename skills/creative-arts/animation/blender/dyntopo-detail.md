---
id: creative-arts.animation.blender.dyntopo-detail
name: dyntopo-detail
category: creative-arts
field: animation
product: blender
tags: [blender, sculpting, dyntopo, dyntopo-detail, detail-size, detail-flood-fill, dynamic-topology, concept-sculpt]
level: practitioner
status: docs-checked
description: "Sculpt with Blender Dynamic Topology: relative, constant, brush and manual detailing, detail sampling, refine methods, Detail Flood Fill and attribute limits."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tool_settings/dyntopo.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/introduction/adaptive.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tool_settings/symmetry.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# dyntopo-detail

Goal: concept sculpting where topology is added only where the brush needs it: horns, tentacles, shapes grown from a sphere.

## Enable

Sculpt Mode > Sidebar > Tool > Dyntopo panel; the checkbox toggles Dynamic Topology. With it active most brushes subdivide the mesh during the stroke. Custom attributes such as Color Attributes, UV Maps and Face Sets are lost or corrupted, so use it on a sculpt-only mesh. Dyntopo and the Voxel Remesher are mutually exclusive and share the same shortcuts.

## Detailing modes

- **Relative Detail**: detail size in screen pixels; zoom out for big details, zoom in for fine ones.
- **Constant Detail**: uniform across the object; the value is a divisor of a Blender unit, so higher means finer.
- **Brush Detail**: detail as a percentage of the brush size; full detail makes topology about the size of the brush radius.
- **Manual Detail**: a uniform percentage that only takes effect when you run Detail Flood Fill.
- **Detail Size / Percentage / Resolution**: set in the panel, or press **R** in the viewport for an interactive preview of the density. **Sample Detail Size** (eyedropper) picks the value from a mesh area when using Constant Detail.
- **Refine Method**: *Subdivide Edges*, *Collapse Edges* or *Subdivide Collapse* (both).
- **Topology Rake** (brush setting): aligns edges with the stroke direction while tessellating; it can cost a lot of performance and suits low-poly meshes.

## Detail Flood Fill

With Constant or Manual detailing, **Detail Flood Fill** (Ctrl-R) fills the whole object with uniform detail at the current resolution.

## Workflow

1. Start from a sphere with Dyntopo on and block shapes with brushes that work well with it (Snake Hook, Clay Strips, Density).
2. Raise the detail for secondary forms; use Detail Flood Fill to even out density.
3. When forms are settled, switch to the Voxel Remesher or retopologize, or move to Multires for detail layers.

## Gotchas

- Slower performance and limited support for some sculpt mode features.
- Dyntopo can leave a mesh asymmetric; use Symmetrize (Symmetry panel, with Direction and Merge Distance) to mirror one half.
- Keep UVs and colours for a later stage, after Dyntopo.

## Verify

Strokes add detail only under the brush; after Detail Flood Fill the wireframe overlay shows even density.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release branch). Confirmed against sculpt_paint/sculpting/tool_settings/dyntopo, introduction/adaptive and symmetry: panel location, the four detailing modes and their meaning, Refine Method names, R and Ctrl-R shortcuts, Sample Detail Size for Constant Detail, Topology Rake performance note, attribute loss, mutual exclusion with voxel remesh, Symmetrize in the Symmetry panel. Removed the unconfirmed Ctrl-D toggle, sample resolution numbers, a Smooth Shading toggle claim and the undo memory remark.
Method: documentation only; no commands were run.
