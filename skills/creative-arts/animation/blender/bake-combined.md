---
id: creative-arts.animation.blender.bake-combined
name: bake-combined
category: creative-arts
field: animation
product: blender
tags: [blender, bake-combined, combined-bake, lightmap-bake, texture-baking, cycles-bake, lightmap-uv]
level: practitioner
status: docs-checked
description: "Bake full lighting into textures with Cycles: Combined bake contributions, lightmaps on a second UV map, view-dependent effects, samples and exposure for real-time use."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/baking.html
  - https://projects.blender.org/blender/blender/src/branch/blender-v5.2-release/intern/cycles/blender/addon/ui.py
  - https://projects.blender.org/blender/blender/src/branch/blender-v5.2-release/source/blender/editors/object/object_bake_api.cc
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# bake-combined

Goal: pre-lit textures or lightmaps for real-time scenes (web, mobile, VR) that look like the Cycles render.

## Combined bake

Render Properties → Bake → *Bake Type: Combined*. The manual describes it as all materials, textures and lighting except specularity, with the contributing passes toggled individually under *Influence*:
- *Lighting*: Direct and/or Indirect.
- *Contributions*: Diffuse, Glossy, Transmission, Emit. These are only active while Direct or Indirect is on, and a Combined bake needs Emit or at least one of Direct/Indirect, otherwise Blender reports an error.
- *View From* (Above Surface or Active Camera) sets the source of reflection ray directions; it is available for Combined, Diffuse, Glossy, Transmission, Shadow and Emit bakes, and the setting is inactive when the scene has no camera.

For a pure lightmap (lighting without albedo) bake *Diffuse* with *Direct + Indirect* ticked and *Color* unticked: without *Color* you get the direct and indirect contributions in gray-scale.

## Lightmap UVs

1. Add a second UV map (Object Data → UV Maps → `+`), name it `Lightmap`.
2. Unwrap it with no overlaps, one atlas for many objects (see `creative-arts.animation.blender.uv-unwrapping`).
3. Make `Lightmap` the **active** UV map for the bake (the bake uses the active UV map).
4. Bake with *Clear Image* on for the first object and off for the rest, or bake all selected at once.

## Quality

- Cycles uses the render settings (samples, bounces) for baking, so the baked quality matches the rendered scene; denoise afterwards in the compositor if needed.
- Use a margin big enough to avoid seams under texture filtering and mip-mapping (`creative-arts.animation.blender.bake-margin`).
- Use a 32-bit float image and save EXR if the engine applies exposure or tonemapping, so highlights do not clip.

## Gotchas

- Glossy and transmission depend on the viewing direction; set *View From* deliberately, or keep specular in the real-time shader.
- Emission and lights must be renderable for the bake to include them.

## Verify

Apply the lightmap in an Emission-only material in EEVEE (or the engine) and compare against a Cycles render from the same camera: same light distribution, no seams along UV borders.

## Checked

2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch) and the 5.2 source UI scripts. Confirmed: Combined definition, Lighting and Contributions toggles, grey-scale result without Color, View From (baking page); contributions active only with Direct/Indirect, View From visibility and the Combined error condition (ui.py, object_bake_api.cc); active UV layer (bake operator). Removed unsupported sample counts, margin sizes, colour-management and "bake never denoises" claims.

Method: documentation only; no commands were run.
