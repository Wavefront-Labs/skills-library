---
id: creative-arts.animation.blender.mask-filter
name: mask-filter
category: creative-arts
field: animation
product: blender
tags: [blender, sculpting, mask-filter, mask-grow, mask-shrink, mask-sharpen, mask-contrast, mask-extract, masking]
level: practitioner
status: docs-checked
description: "Refine sculpt masks with Mask Filters (smooth, sharpen, grow, shrink, contrast), mask Expand, invert/clear, and Mask Extract/Slice to turn masks into new geometry."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/editing/mask.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/editing/expand.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# mask-filter

Goal: clean, controllable masks, the selection system of sculpt mode.

## Mask menu essentials (Sculpt Mode > Mask menu)

- **A** opens the mask pie menu. In the pie: **Ctrl I** invert, **Alt M** clear. **B** is Box Mask and **Ctrl RMB** is Lasso Mask. Fill Mask masks all visible geometry.
- **Mask Filters** (Smooth/Sharpen Mask, Grow/Shrink Mask, Increase/Decrease Contrast): operate on the whole mask. Smooth/Sharpen changes the sharpness of the mask edge. In the Adjust Last Operation panel, **Iterations** and **Auto Iteration Count** (automatic count based on the number of vertices) control strength. **Shift R** (Repeat Last) is an alternative to iterations.
- **Expand Mask by Topology** (**Shift A**) and **Expand Mask by Normals** (**Shift Alt A**): see the Expand page for the modal keys. See `sculpt-masking-facesets` for face-set expansion.
- **Mask from Cavity**, **Mask from Mesh Boundary**, **Mask from Face Sets Boundary**, **Mask by Color**: generate masks, with Mode (Mix by default) and Mix Factor in the Adjust Last Operation panel.
- **Random Mask**: Per Vertex, Per Face Set or Per Loose Mask.

## Turning masks into geometry

- **Mask Extract**: duplicates the masked area as a new mesh object. Options: Threshold, Add Boundary Loop, Smooth Iterations, Project to Sculpt, and **Extract as Solid** (adds a Solidify modifier to the new object).
- **Mask Slice**: removes the masked vertices from the mesh. Options: Threshold, **Fill Holes**, **Slice to New Object**.

## Workflow tip

Paint a rough mask, Sharpen Mask for a few iterations, Smooth Mask once, then Mask Extract with Extract as Solid and refine the new piece with modifiers such as Remesh.

## Gotchas

- Masks are per vertex, so low-resolution meshes give jagged masks; filters will not fix mesh resolution.
- Clear Sculpt-Mask Data (Properties > Object Data > Geometry Data) frees the mask layer entirely.

## Verify

The mask overlay (Viewport Overlays > Sculpt > Mask, which also sets its opacity) shows the expected boundary, and the extracted mesh is closed with an even thickness.

## Checked

Date 2026-10-27. Blender manual 5.2 (blender-v5.2-release RST).
Confirmed: Mask pie menu shortcut is A (not M); Ctrl I invert and Alt M clear inside the pie; Shift A and Shift Alt A expand shortcuts; Mask Filter types, Iterations, Auto Iteration Count; Mask Extract and Mask Slice options; Mask from Cavity, Mesh Boundary, Face Sets Boundary, by Color, Random Mask names; overlay location; Clear Sculpt-Mask Data location.
Removed as unconfirmed: the `.sculpt_mask` attribute name, remesh Preserve Attributes advice, the Thickness option of Mask Extract (replaced by Extract as Solid), the "4.x" version label, and the example iteration and thickness numbers.
Method: documentation only; no commands were run.
