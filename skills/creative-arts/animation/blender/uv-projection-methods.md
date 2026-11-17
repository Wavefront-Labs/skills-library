---
id: creative-arts.animation.blender.uv-projection-methods
name: uv-projection-methods
category: creative-arts
field: animation
product: blender
tags: [blender, uv, unwrap, uv-projection-methods, project-from-view, cylinder-projection, cube-projection, sphere-projection]
level: practitioner
status: docs-checked
description: "Quick Blender UV projections: Cube, Cylinder (direction, pole, radius), Sphere, Project from View (Bounds), Follow Active Quads and Reset, with options and limitations."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/uv.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# uv-projection-methods

Goal: fast, predictable UVs for simple shapes and for projected textures.

## `U` menu projections (Edit Mode; UV menu in the 3D Viewport or UV Editor)

- **Cube Projection**: projects each selected face onto the most suitable side of a virtual cube centred on the pivot point and aligned to local axes; the sides overlap in the UV map (use Pack Islands to separate). Options: Cube Size, Correct Aspect, Clip to Bounds, Scale to Bounds.
- **Cylinder Projection**: projects onto a virtual cylinder, then unrolls it. Options: Direction/Align (View on Equator, View on Poles, Align to Object; Polar ZX/ZY), Pole (Pinch or Fan), Preserve Seams, Radius (half the cylinder's height), Correct Aspect, Clip/Scale to Bounds.
- **Sphere Projection**: projects onto a virtual sphere and flattens it like a world map; useful for eyes or planets. Same Direction, Align, Pole, Preserve Seams, Correct Aspect and bounds options.
- **Project from View** (3D Viewport): projects onto the view plane so the UV map is a wireframe picture of the mesh from the current viewing angle; stretches where the model recedes. Options: Orthographic, Camera Bounds (only effective when viewing through the camera), Correct Aspect, Clip/Scale to Bounds. **Project from View (Bounds)** is the same with Scale to Bounds on by default.
- **Follow Active Quads**: starts from the active quad's existing UV quad and attaches neighbouring selected quads; non-quads are ignored. *Edge Length Mode*: Even, Length, Length Average. Give the active quad a good UV shape first, and Pack Islands if the result goes out of bounds.
- **Reset** (`U` > Reset) fills the whole UV area with each selected face.

## Correct Aspect

Needs a material with an Image Texture node that is the selected node in the Shader Editor.

## Gotchas

- View-based options depend on the 3D Viewport view; set the view first or use Align to Object.
- Only the cylinder and sphere projections have Preserve Seams; others ignore seams.

## Verify

A UV Grid or Color Grid test image reads correctly on the main visible faces; the Display Stretch overlay is acceptable.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch, projects.blender.org/blender/blender-manual). Confirmed against the UV Operators page: all projection options, definitions and shortcuts. Removed unconfirmed claims about eyeball seam and pole placement and the 'when projections win' list.
Method: documentation only; no commands were run.
