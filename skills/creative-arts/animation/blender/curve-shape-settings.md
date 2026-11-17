---
id: creative-arts.animation.blender.curve-shape-settings
name: curve-shape-settings
category: creative-arts
field: animation
product: blender
tags: [blender, curve-object, curve-fill-mode, curve-resolution, curve-twist, curve-2d, shape-panel]
level: practitioner
status: verified
description: "Configure Blender curve Shape: 2D vs 3D Dimensions, Fill Mode, Resolution Preview/Render U, Twist Method and Smooth, Fill Solver and Rule, Curve Deform options."
sources:
  - https://docs.blender.org/manual/en/5.2/modeling/curves/properties/shape.html
  - https://docs.blender.org/manual/en/5.2/modeling/curves/editing/curve.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# curve-shape-settings

Goal: curves that fill, twist and tessellate as intended, and render at a different density than they display.

## Properties > Data > Shape

- **Dimensions** (2D / 3D): curves added from the Add menu are 3D (control points anywhere in space; `bpy.data.curves.new` gives `'2D'`, so set `dimensions` yourself). 2D constrains control points to the curve's local XY plane; a closed 2D curve creates a renderable flat face.
- **Resolution Preview U / Render U**: number of points computed between every pair of control points. Preview U is used in the 3D Viewport; Render U is used for rendering, and if Render U is 0 the Preview U value is used for both.
- **Twist Method**: Minimum, Tangent or Z-Up. A 3D curve has a twist that affects the normals. **Smooth** interactively removes kinks from over-twisting (for example after converting meshes to curves).
- **Fill Mode** (how a beveled or 2D curve is displayed): for 3D curves *Full*, *Back*, *Front*, *Half* (half a cylinder); for 2D curves *None*, *Back*, *Front*, *Both*.
- **Fill Solver**: *Sweep Line* (fast, no self-intersecting curves) or *Delaunay* (Constrained Delaunay Triangulation, supports self-intersections, slower). Blender 4.5.14 has no solver or rule property on `Curve`, so these two entries and Fill Rule are from the 5.2 manual only.
- **Fill Rule** (Delaunay only): *Even-Odd* (overlaps may cancel out) or *Non-Zero* (same winding direction fills as a union, opposite directions create holes).
- **Curve Deform** (used with a curve as path or the Curve modifier): *Radius* scales the deformed object by the curve radius; *Stretch* stretches or squeezes the mesh over the whole curve; *Bounds Clamp* ignores the object and mesh offset along the deformation axis (use it with Stretch or a negative axis).

## Typical setups

- Logo: 2D curve, Fill Mode Both, Extrude for depth, a small Bevel Depth (see curve-bevel).
- Gutter: 3D, Fill Mode Half with a Round bevel.

## Gotchas

- Switching a curve from 3D to 2D constrains points to local XY (tested: `dimensions = '2D'` set every point's Z to 0).
- Higher Resolution multiplies the geometry; keep Preview U low while working and raise Render U only on hero assets (Render U = 0 means "same as preview").

## Verify

Change Render U, render a test region, and compare with the viewport, which uses Preview U only.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (curve Shape panel, curve editing pages) and 5.2 source enum definitions for Fill Mode and Twist Method. Confirmed: Dimensions, Preview/Render U rule, Twist Method options and Smooth, 2D and 3D Fill Mode items, Fill Solver, Fill Rule, Curve Deform options. Removed as unconfirmed: default twist method, example resolution numbers, memory advice, and the claim that switching 3D to 2D discards tilt.
Run check, 2026-11-01, Blender 4.5.14 LTS headless: `dimensions` items 2D and 3D, a data-API curve defaults to 2D and the Add-menu primitives to 3D, switching to 2D zeroed Z; `resolution_u` default 12 and `render_resolution_u` default 0; `twist_mode` items Z_UP, MINIMUM, TANGENT and `twist_smooth`; fill modes 3D FULL, BACK, FRONT, HALF and 2D BACK, FRONT, BOTH, NONE; `use_radius`, `use_stretch`, `use_deform_bounds` exist. Unrun: Fill Solver and Fill Rule (not in 4.5.14), Render U = 0 meaning Preview U at render time, Curve Deform effects, UI panel layout.

Method: documentation checked against the manual and API pages; the code was run headless in Blender 4.5.14.
