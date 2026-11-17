---
id: creative-arts.animation.blender.normal-bump-nodes
name: normal-bump-nodes
category: creative-arts
field: animation
product: blender
tags: [blender, shader, normal-bump-nodes, normal-map-node, bump-node, tangent-space]
level: practitioner
status: docs-checked
description: "Use Normal Map and Bump nodes in Blender correctly: tangent vs object space, Non-Color images, strength, DirectX vs OpenGL green channel and chaining."
sources:
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/displacement/normal_map.html
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/displacement/bump.html
  - https://developer.blender.org/docs/release_notes/4.5/cycles/
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# normal-bump-nodes

## Normal Map node

1. Image Texture with the normal map, Color Space **Non-Color** (needed for tangent space maps).
2. Image Color -> Normal Map **Color**; Normal Map output -> BSDF **Normal**.
3. **Space**: Tangent (most common; supports object transformation and deformation), Object, or World. For tangent space the **UV Map** field must match the UV map the image uses.
4. **Strength** scales the effect.
5. **Convention**: OpenGL (Y up in the green channel) is the default for rendering and baking; choose DirectX for maps from software that assumes Y points down.
6. **Base** (relevant with displacement): Original Base (smooth undisplaced surface, for matching normal and displacement maps) or Displaced Base (add the normal map on top of displacement).

## Bump node

- Inputs **Height**, **Strength**, **Distance** (multiplier on the height value), **Filter Width** (in pixels, default 0.1; larger values give a bevel-like effect on stepped textures; fixed value only), **Normal**; property **Invert**.
- Chain: Normal Map output -> Bump **Normal** input -> BSDF Normal, so bump adds fine detail on top of the normal map.
- Filter Width was added in 4.5 per the Cycles release notes.
- With no Height connected the node passes its Normal through unchanged.

## Gotchas

- A tangent-space normal map left as sRGB shades wrongly.
- Bump only fakes shading and the silhouette is unchanged (use the Displacement node).
- Bump maps should use Cubic image interpolation to avoid stepping.

## Verify

Rotate a light around the object: highlights move consistently with the detail; with the wrong Convention the lighting appears to come from the wrong side.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch, docs.blender.org manual en/5.2). Confirmed against displacement/normal_map and displacement/bump (spaces, Convention, Base, UV Map, Bump inputs and Filter Width default 0.1, no-op behaviour) and the 4.5 Cycles release notes (Bump Filter Width added in 4.5, not 4.1 as the draft said). Removed the nonexistent 'Blender Object/World' spaces and the manual green-channel inversion recipe.

Method: documentation only; no commands were run.
