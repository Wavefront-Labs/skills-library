---
id: creative-arts.animation.blender.sculpt-masking-facesets
name: sculpt-masking-facesets
category: creative-arts
field: animation
product: blender
tags: [blender, sculpt-masking, sculpt-mask, face-sets, auto-masking, mask-slice, mask-extract, mask-by-color, expand, trim-tools, sculpt, sculpting, isolation]
level: advanced
status: docs-checked
description: "Control what a Blender sculpt stroke touches: mask brush, Expand, Face Sets, auto-masking, Mask Slice and Extract, Mask by Color, and mask attributes."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/editing/mask.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/editing/face_sets.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/editing/expand.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/editing/sculpt.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/controls.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/attributes_reference.html
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# sculpt-masking-facesets

Goal: sculpt only where you mean to. Masks are per-vertex values (a Float attribute on points); Face Sets are per-face integer IDs. Both persist in the mesh and both feed auto-masking.

## Mask basics

- **Mask brush** (M): paints a selection of the mesh that other brushes leave unaffected; shown as a grey-scale overlay. Alt-LMB toggles it temporarily, Ctrl-Alt-LMB temporarily erases. Hold Shift with the Mask brush to smooth the mask. LMB adds to the mask and Ctrl-LMB subtracts.
- Masking is the inverse of selecting: masked vertices cannot be edited, so to edit masked areas use Invert Mask.
- **A pie menu** and the Mask menu: *Invert Mask* (Ctrl-I), *Fill Mask*, *Clear Mask* (Alt-M), *Mask Filters* (Smooth/Sharpen, Grow/Shrink, Increase/Decrease Contrast; Iterations and Auto Iteration Count in Adjust Last Operation, Shift-R repeats), *Box Mask* (B; Shift or MMB clears), *Lasso Mask* (Ctrl-RMB), Line and Polyline Mask tools (see `creative-arts.animation.blender.box-lasso-mask`), *Mask by Color*, *Random Mask* (per vertex, face set or loose part).
- **Mask from Cavity**, **Mask from Mesh Boundary** and **Mask from Face Sets Boundary** generate masks procedurally, with Mode (mix with existing mask), Mix Factor and the Auto-Masking settings in the Adjust Last Operation panel.
- Display: Viewport Overlays > Sculpt > Mask opacity. **Clear Sculpt-Mask Data** (Properties > Object Data > Geometry Data) frees the mask layer.

## Expand (Shift-A mask by topology, Shift-Alt-A mask by normals, Shift-W face set)

A modal operator that expands from the vertex under the cursor; confirm with LMB or Return. Keys while it runs:
- 1 Geodesic, 2 Topology, 3 Diagonals, 4 Spherical falloff. Starting on an open boundary expands from the whole boundary loop with Topology falloff.
- **F** invert, **E** toggle preserve state (accumulate or replace; for face sets, toggles creating boundaries versus replacing), **Space** moves the origin.
- **G** linear gradient, **B** brush falloff gradient; **R** and **Alt-R** geodesic and topology recursion steps; **W** and **Q** add or remove loops; **Y** and **T** change texture distortion (a texture needs 3D mapping).
- **Ctrl** snaps the expansion to the face set under the cursor; moving the cursor outside the mesh masks the whole connected mesh.
- Expand only affects visible geometry. Expanding from a face set boundary or using Snap to Face Sets masks regions exactly.

## Face Sets

- Create: **Draw Face Sets** brush (Ctrl continues the set under the cursor, Shift relaxes borders); Face Sets menu entries Face Set from Masked, Visible, Edit Mode Selection; **Initialize Face Sets** by Loose Parts, Face Set Boundaries, Materials, Normals, UV Seams, Edge Creases, Edge Bevel Weight, Sharp Edges (with Threshold).
- Edit: Edit Face Set tool Grow (Ctrl-W), Shrink (Ctrl-Alt-W), Delete Geometry, Fair Positions, Fair Tangency; Expand Face Set (Shift-W). The Alt-W pie holds the face set operations.
- Visibility: **H** hides the face set under the cursor, **Shift-H** isolates it (or shows everything if sets are hidden), **Alt-H** or **W** shows all; Invert Visible, Hide Masked and Grow/Shrink Visibility (PageUp, PageDown) are in the Sculpt menu. Hiding is shared by all modes except Object Mode.
- Overlay opacity: Viewport Overlays > Sculpt > Face Sets; Randomize Colors reshuffles display colours.
- Voxel remesh keeps them with Preserve > Face Sets; Dyntopo loses or corrupts them, so create sets after your final remesh.

## Auto-masking (header popover or Alt-A pie)

Topology, Face Sets, Mesh Boundary, Face Sets Boundary (Propagation Steps), Cavity (Factor, Blur, Custom Curve) and Cavity (Inverted), View Normal (Limit, Falloff, Occlusion), Area Normal. All can be combined and also set per brush. Details in `creative-arts.animation.blender.auto-masking-options`.

## Mask-derived modelling operators

- **Mask Extract** (Mask menu): duplicates masked geometry as a new object, with Threshold, Add Boundary Loop, Smooth Iterations, Project to Sculpt and Extract as Solid (adds a Solidify modifier). Good for armour plates and clothing shells.
- **Mask Slice**: removes the masked vertices; Fill Holes fills the result (with nothing masked it just fills holes); Slice to New Object creates a new object from the masked geometry; Threshold.
- **Trim tools**: Box, Lasso, Line and Polyline Trim (see `creative-arts.animation.blender.sculpt-trim-tools`).
- **Attributes**: the mask is the `sculpt_mask` attribute (Float, Point domain) and face sets are `sculpt_face_set` (Integer, Face domain), listed in the Attributes Reference.

## Workflow patterns

1. Block the model, voxel remesh at working resolution, run Initialize Face Sets by Loose Parts, then paint sets for arm, torso, head and hands.
2. Sculpt regions with Face Sets auto-masking; hide sets to reach hidden areas.
3. Details: Cavity auto-masking plus Scrape and Crease brushes.
4. Clothing: mask a region, Mask Extract with Extract as Solid.

## Gotchas

- Masked vertices cannot be edited, so a brush that seems to do nothing may be blocked by a leftover mask (Clear Mask, Alt-M); the mask overlay opacity can be raised to see it.
- Auto-masks are never shown as an overlay; use the Create Mask buttons to visualize them.

## Verify

- With a mask over half the model, a Grab stroke leaves the masked half unmoved.
- A Clay stroke across two face sets with Face Sets auto-masking affects only the set you started on.
- H hides the set under the cursor; Alt-H restores all.
- Mask Extract produces a separate object from the masked region.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release branch). Confirmed against sculpt_paint/sculpting/editing (mask, face_sets, expand, sculpt), controls, brushes list, introduction/visibility_masking_face_sets and the Geometry Nodes Attributes Reference. Corrected: Lasso Mask is Ctrl-RMB; Expand keys (F invert, E preserve, Ctrl snap to face sets; there are no 5, 6, 7 falloff keys); Face Set from Masked has no Ctrl-W shortcut (Ctrl-W grows a face set); attribute names are sculpt_mask and sculpt_face_set without a leading dot. Removed unconfirmed claims: version gates (4.0+, 4.2+), the Python snippet, Spreadsheet Show Internal, export remarks and Mask Extract on Multires behaviour.
Method: documentation only; no commands were run.
