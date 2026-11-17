---
id: creative-arts.animation.blender.bake-ao
name: bake-ao
category: creative-arts
field: animation
product: blender
tags: [blender, bake-ao, ao-bake, texture-baking, ambient-occlusion, cycles-bake]
level: practitioner
status: docs-checked
description: "Bake ambient occlusion maps in Cycles: AO bake type, AO Distance, samples and noise, and selected-to-active AO from a high poly."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/baking.html
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/light_paths.html
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/input/ao.html
  - https://docs.blender.org/manual/en/latest/compositing/types/filter/denoise.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# bake-ao

Goal: a clean AO texture for game assets, texture painting masks or multiplying into base colour.

## Setup

1. Target image: Non-Color data, held by the active, selected Image Texture node in each material (nothing is baked for a material without one; see `creative-arts.animation.blender.bake-clear-image`).
2. Render Properties → Bake → *Bake Type: Ambient Occlusion*. The manual describes it as AO "as specified in the World panels", ignoring all lights in the scene.
3. In 5.2 the world's AO settings (*AO Factor*, *AO Distance*) are shown under Render Properties → Light Paths → Fast GI Approximation; AO Distance is the distance from the shading point to trace rays. A shorter distance emphasises nearby features, a longer one takes farther objects into account.
4. Cycles bakes with the scene's render settings (samples, bounces), so raise Sampling → Render → Max Samples if the AO map is noisy.
5. *Bake*.

## Only the object, or the environment too

The bake traces against the scene. For an asset texture, hide other objects from render (camera icon) or bake in an isolated scene; otherwise neighbouring geometry can darken the result.

## High to low

Enable *Selected to Active*, select the high poly, then shift-select the low poly (active). Rays are cast from the low-poly object inwards towards the high-poly object; tune *Extrusion* or *Max Ray Distance*, or use a cage (`creative-arts.animation.blender.bake-cage`).

## Noisy AO

Raise samples, or denoise the saved image in the compositor with a Denoise node. The Denoise node's *Prefilter: None* assumes noise-free input and keeps any remaining noise, so use *Fast* or *Accurate* for a noisy AO map (*Accurate* usually keeps more detail but is slower).

## Gotchas

- The *Ambient Occlusion* shader node (Distance, Samples, Inside, Only Local) is a shading node used for procedural texturing; the bake type is separate.
- Overlapping or mirrored UVs bake both sides into the same pixels; offset mirrored islands before baking, then move them back.

## Verify

AO map is white on open surfaces and darkens only in creases and contact areas; no speckle at 100% zoom.

## Checked

2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch) and the 5.2 source UI scripts. Confirmed: Bake Type Ambient Occlusion wording and Selected to Active ray direction (baking page); AO Factor and AO Distance live under Light Paths > Fast GI Approximation (light paths page and ui.py); Denoise node Prefilter None/Fast/Accurate meaning (denoise page); AO node properties (AO node page). Removed unsupported claims (sample counts, "bake ignores denoiser", world-panel path).

Method: documentation only; no commands were run.
