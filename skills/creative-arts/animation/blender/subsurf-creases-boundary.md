---
id: creative-arts.animation.blender.subsurf-creases-boundary
name: subsurf-creases-boundary
category: creative-arts
field: animation
product: blender
tags: [blender, subsurf-creases, boundary-smooth, uv-smooth, edge-creases, crease, subdivision-surface, hard-surface]
level: practitioner
status: verified
description: "Control subdivision sharpness and UVs in Blender: edge and vertex creases, Use Creases, Boundary Smooth (All vs Keep Corners) and UV Smooth modes."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/subdivision_surface.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/edge/edge_data.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/vertex/vertex_crease.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# subsurf-creases-boundary

Goal: sharpen subdivided edges without extra support loops, and keep open borders and UVs from drifting.

## Creases

- **Edge crease**: select edges, *Edge > Edge Crease* (**Shift E**), then move the mouse or type a number, which is added to the existing value (positive or negative). The value also shows in the Sidebar.
- **Vertex crease**: *Vertex > Vertex Crease* sets how sharp the vertex's corner is; the value can also be changed in the Sidebar's Transform panel.
- Modifier > Advanced > **Use Creases** must be on for the stored crease values to take effect. *Quality* (with *Use Limit Surface*) affects how accurately edge creases work.
- Show them: Mesh Edit Mode overlays > *Creases*.

When to use creases vs holding edges: creases keep topology light, but they are crease values rather than geometry. Use support loops (see `hard-surface-modeling`) when the asset leaves Blender or needs a bevel-like radius.

## Boundary Smooth

- **All**: smooth boundaries, including corners.
- **Keep Corners**: smooth boundaries, but corners are kept sharp.

## UV Smooth

- **None**: UVs are not smoothed and boundaries stay sharp (a kinked UV boundary kept its exact points).
- **Keep Corners**: UVs are smoothed and only the corners of discontinuous boundaries are kept sharp. A kinked boundary point was still smoothed in 4.5.14 (v 0.2 moved to 0.133), so the boundary does not stay unchanged; use Keep Boundaries for that.
- **Keep Corners, Junctions** and **Keep Corners, Junctions, Concave**: UVs are smoothed, with progressively more corners and junctions kept sharp.
- **Keep Boundaries**: UVs are smoothed, boundaries are kept sharp.
- **All**: UVs and their boundaries are smoothed.
- If a texture "swims" after subdivision, the UV Smooth mode is the first thing to check.

## Gotchas

- Edge Crease adds to the existing value, so type a negative number to reduce or clear it.

## Verify

Toggle Use Creases and watch the edge sharpen and soften; compare UV Smooth modes on a textured mesh.

## Checked

2026-10-27, Blender manual 5.2 (blender-v5.2-release RST: Subdivision Surface modifier, Edge Data, Vertex Crease and Viewport Overlays pages). Confirmed: Edge > Edge Crease on Shift E adds a positive or negative value; Vertex > Vertex Crease; Use Creases, Use Limit Surface and Quality in Advanced; Boundary Smooth All and Keep Corners; the UV Smooth options list; Creases overlay under Mesh Edit Mode overlays. Corrected: Shift V is not vertex crease (the operator has no shortcut in the manual); UV Smooth None leaves UVs unchanged; Keep Corners keeps corners sharp. Removed as unconfirmed: the crease_edge attribute, the 0.9 render-level figure, the magenta colour, exporter and Multires claims and the Use Creases default.

Run check, 2026-11-01, Blender 4.5.14 LTS headless: Subdivision Surface with Python: Boundary Smooth has Keep Corners and All (a plane corner stays at 2.0 with Keep Corners and rounds to 1.836 with All); UV Smooth has None, Keep Corners, Keep Corners Junctions, Keep Corners Junctions Concave, Keep Boundaries and All; on a UV island with a kinked boundary point, None and Keep Boundaries kept it (0.2), Keep Corners and the Junction modes smoothed it (0.133), and All also moved the island corners (0.082 to 1.918); Use Creases with crease value 1 on all edges gave a sharper result (x extent 1.0 against 0.84 when off); Use Limit Surface and Quality (1 to 10, default 3) exist; the Edge Crease operator adds to the stored value (0.5 then 0.25 gave 0.75, then -1 clamped to 0); the default keymap has Shift E for Edge Crease and no key for Vertex Crease. Not run: the Sidebar crease fields and the Creases overlay (UI).

Method: manual text confirmed from documentation; behaviour run headless in Blender 4.5.14.
