---
id: computing-software.computer-graphics-engineering.graphics-math.cube-map-face-projection
name: cube-map-face-projection
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, projection, cubemap-face-projection, cube-map, environment-map, equirectangular, shadow-cubemap]
level: practitioner
status: draft
description: "Work with cube map faces: direction-to-face/uv selection rules, 90-degree per-face view/projection matrices, face orientation conventions, seams and equirect conversions."
sources: ["https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf", "https://learn.microsoft.com/en-us/windows/win32/direct3d9/cubic-environment-mapping", "https://www.khronos.org/opengl/wiki/Cubemap_Texture"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cube map face projections

## Direction -> face and uv (GL spec table)
Pick the major axis (largest |component|):
| Face | Major | sc | tc | ma |
|---|---|---|---|---|
| +X | rx | -rz | -ry | rx |
| -X | rx | +rz | -ry | rx |
| +Y | ry | +rx | +rz | ry |
| -Y | ry | +rx | -rz | ry |
| +Z | rz | +rx | -ry | rz |
| -Z | rz | -rx | -ry | rz |
`u = (sc / |ma| + 1) / 2`, `v = (tc / |ma| + 1) / 2`. These conventions come from RenderMan and make
faces look "upside down" compared to a naive camera; reproduce them exactly when writing faces.

## Rendering into faces
Each face: 90-degree vertical FOV, aspect 1, camera at the probe centre looking along the face axis
with these up vectors (GL convention): +X up -Y, -X up -Y, +Y up +Z, -Y up -Z, +Z up -Y, -Z up -Y.
Render with a single pass using layered rendering (`gl_Layer`, `SV_RenderTargetArrayIndex`) or
multiview, or six passes.

## Seams
- Enable seamless filtering: `glEnable(GL_TEXTURE_CUBE_MAP_SEAMLESS)` (always on in D3D11+/Vulkan).
- Prefiltered mip chains (IBL) need filtering across faces, otherwise visible edges at rough mips.

## Point light shadow cubes
Store linear distance (or use a depth cube with a per-face projection) and compare with
`length(fragPos - lightPos)`; avoids inconsistent depth between faces.

## Equirect <-> cube
For each cube texel, compute its direction (inverse of the table), convert to longitude/latitude
`(atan2(x, -z), asin(y))` with your engine's convention, and sample. Watch for orientation and
handedness differences between tools (cmgen, Blender, three.js PMREM).

## Verify
Render a cube map of a scene with labelled axes (coloured +X/+Y/+Z markers), sample along known
directions and check the right colour comes back; check across face edges for seams.
