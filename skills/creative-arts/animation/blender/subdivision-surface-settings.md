---
id: creative-arts.animation.blender.subdivision-surface-settings
name: subdivision-surface-settings
category: creative-arts
field: animation
product: blender
tags: [blender, subdivision-surface, catmull-clark, simple-subdivision, subsurf-levels, render-levels, optimal-display, gpu-subdivision, opensubdiv, modifiers]
level: practitioner
status: docs-checked
description: "Set up Blender's Subdivision Surface modifier: Catmull-Clark vs Simple, viewport vs render levels, Quality, Optimal Display, Simplify cap and GPU subdivision."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/subdivision_surface.html
  - https://docs.blender.org/manual/en/latest/editors/preferences/viewport.html
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/simplify.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# subdivision-surface-settings

Goal: smooth, fast subdivision that looks the same in viewport and render without wasting memory.

## Catmull-Clark vs Simple

- **Catmull-Clark**: subdivides and smooths the surfaces for a more pleasant-looking mesh. Use for subd modeling.
- **Simple**: only subdivides; it often gives no smoothing unless the surface is non-coplanar (like the Subdivide operator in Edit Mode). The manual suggests it, for example, to increase base mesh resolution before using displacement maps.
- Shortcut: select objects and press `Ctrl 1`, `Ctrl 2`, `Ctrl 3` and so on to add a Subdivision Surface modifier with that many Viewport levels; the Render levels are not changed.
- The modifier uses the OpenSubdiv library as its backend. It does not let you edit the new geometry without applying it; the Multiresolution modifier does (in Sculpt Mode).

## Levels

- **Levels Viewport** and **Render**: the number of levels shown in the 3D Viewport and in the final render. Higher levels mean more vertices and more system and video memory, and can hang or crash Blender if memory runs out. Keep Viewport low and Render higher, and do not set Viewport above Render (the manual's tip). Each level splits every quad into four (for all-quad meshes).
- **Advanced**: *Use Limit Surface* places vertices on the surface of infinite subdivision; *Quality* controls how precisely vertices sit on it when Use Limit Surface is enabled (lower is faster, higher is not necessarily visibly better, and it affects the accuracy of edge creases); *UV Smooth*, *Boundary Smooth*, *Use Creases* and *Use Custom Normals* are also listed there.
- Render Properties > Simplify > *Max Subdivision* sets the maximum number of subdivisions of Subdivision Surface modifiers (Cycles and EEVEE simplify pages); check it before the final render if it was used.

## Optimal Display

When rendering the wireframe of the object, skips the wires of the new subdivided edges and shows only the edges of the original geometry. Purely visual.

## GPU subdivision (OpenSubdiv)

- Preferences > Viewport > Subdivision > **GPU Subdivision**: under certain circumstances the GPU subdivides a mesh with a Subdivision Surface modifier, which typically increases subdivision performance. When enabled, normals and tangents are interpolated instead of being recomputed after smoothing, which can change shading compared with the CPU implementation.
- The manual does not list the exact circumstances; a modifier stack that needs CPU-evaluated geometry after Subdivision Surface may prevent it (practice, test on your file).
- *Adaptive Subdivision* (Cycles only) subdivides by distance to the camera, using Pixel or Object space; Object space is required for instanced meshes.

## Gotchas

- The modifier's position in the stack affects the result (order of execution); a Subdivision Surface before an Armature means the Armature deforms the denser mesh, which is slower (practice).
- Ngons and triangles subdivide into poles and pinching; keep subd meshes all-quad where it shows (practice).
- Subdivision is a different operation from Smooth Shading.

## Verify

For an all-quad mesh the evaluated face count equals the cage faces times 4 to the power of the level (check in the Statistics overlay); compare playback speed with GPU Subdivision on and off.

## Checked

2026-10-27, Blender manual, branch blender-v5.2-release (raw RST, projects.blender.org/blender/blender-manual). Confirmed against modeling/modifiers/generate/subdivision_surface.rst (Catmull-Clark vs Simple, levels warning and tip, Optimal Display, Use Limit Surface, Quality, Ctrl-N shortcut, adaptive subdivision), editors/preferences/viewport.rst (GPU Subdivision wording and shading note) and render/cycles/render_settings/simplify.rst (Max Subdivision). Removed unconfirmed claims: default mode, suggested level numbers, Quality 3, exact GPU-subdivision stack conditions, Limit Surface legacy behaviour.

Method: documentation only; no commands were run.
