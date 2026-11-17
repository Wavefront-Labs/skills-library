---
id: creative-arts.animation.texturing.normal-map-directx-opengl
name: normal-map-directx-opengl
category: creative-arts
field: animation
product: texturing
tags: [normal-map-convention, texture-export, directx-normal, opengl-normal, green-channel, y-flip, tangent-space, mikktspace, normal-map]
level: practitioner
status: draft
description: "Identify and convert DirectX (Y-) vs OpenGL (Y+) tangent-space normal maps, which renderer expects which, and why tangent basis (MikkTSpace) must match the baker."
sources:
  - https://helpx.adobe.com/substance-3d-painter/technical-support/technical-issues/texturing/normal-map-flipped.html
  - http://www.mikktspace.com/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DirectX vs OpenGL normal maps

**Goal:** bumps that pop out instead of in. Tangent-space normal maps store the surface normal's Y
component in the green channel; DirectX convention has Y pointing down (Y-), OpenGL up (Y+). Using the
wrong one inverts lighting on the vertical axis: lit from below, ridges look like grooves.

## Who expects what

| Target | Convention |
|---|---|
| Blender, Maya (Arnold), Houdini (Karma/Mantra), Unity, glTF | OpenGL (Y+) |
| Unreal Engine, 3ds Max (typically), CryEngine | DirectX (Y-) |
| Substance Painter | project setting (OpenGL or DirectX); exports either via converted maps |

## Recognising

Look at a map of a raised dome or bolt head under neutral display: in OpenGL maps the top edge of a bump
is light green (G high) and the bottom edge dark; DirectX is the reverse. Or simply check in a viewer
with a light from the top: raised details should be lit on top.

## Converting

- Invert the green channel: in Painter export choose "Normal DirectX" or "Normal OpenGL" converted map;
  in Photoshop/GIMP/Krita invert G only; with ImageMagick:
```bash
magick normal_dx.png -channel G -negate +channel normal_gl.png
```
- In Blender a quick fix is Separate Color - invert G - Combine before the Normal Map node, but fixing
  the file is cleaner.

## Tangent basis

Even with the right Y convention, normals bake for a specific tangent basis. Bake and render with the
same one: **MikkTSpace** is the common standard (Blender, Painter default, Unity, Unreal). Mismatched
bases show as faint seams or shading errors on low-poly smoothing.

## Gotchas

- Normal maps must be linear (Non-Color); sRGB interpretation flattens and skews them.
- Mixing conventions in one asset library is common with downloaded assets: tag convention in file names
  (`_nGL`, `_nDX`) or library metadata.

## Verify

Render a test sphere or the asset under a top light: raised details are lit from above; compare against
Painter's viewport with the same convention.
