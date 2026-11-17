---
id: creative-arts.animation.blender.ambient-occlusion-node
name: ambient-occlusion-node
category: creative-arts
field: animation
product: blender
tags: [blender, shader, ambient-occlusion-node, ao-node, bevel-node, edge-wear]
level: practitioner
status: docs-checked
description: "Use Blender's Ambient Occlusion and Bevel shader nodes (Cycles only) for dirt masks, cavity shading and rounded edges without extra geometry."
sources:
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/input/ao.html
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/input/bevel.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# ambient-occlusion-node

## Ambient Occlusion node

- Outputs **Color** (ambient occlusion with colour tint) and **AO** (occlusion factor without tint). Inputs: **Color** (tint), **Distance** (distance up to which other objects count as occluders), **Normal** (default shading normal when unconnected).
- Settings: **Samples** (ray-traced samples; keep as low as possible), **Inside** (detect convex rather than concave shapes by computing occlusion inside the mesh, which gives an edge-wear mask), **Only Local** (Cycles only: only the object itself occludes).
- Dirt: AO -> Color Ramp -> Mix Fac between clean and dirty. Edge wear: Inside on, short Distance -> Color Ramp.
- The manual marks the node Cycles Only. It gives no valid result when the object is a caustic caster or receiver while the scene has active caustic casters, receivers and a shadow caustics light, or when OSL is active with the OptiX backend.
- For occlusion across the whole render use the Ambient Occlusion render pass in the compositor instead.

## Bevel node

- Cycles Only. Rounds edges at shading time like bump mapping: only shading changes, not geometry. Inputs **Radius** (width of the bevel effect) and **Normal** (the normal to bevel on top of, for example from a Bump node); property **Samples** (default 4; more is more accurate but slower, and noise is also resolved by more AA samples). Output **Normal** goes to the BSDF Normal.
- Same caveats as AO: no valid result with the caustics set-up above or OSL on OptiX.
- The Bevel modifier is a faster option when it works but can fail on complex or messy geometry.

## Gotchas

- The AO node is expensive in Cycles; the manual suggests Pointiness from the Geometry node or baked AO when render time matters.
- The Bevel node is very expensive (the manual says it may slow renders by about 20% even in busy scenes); use it for baking or still frames.
- Bevel does not change the silhouette; model real bevels for close-up hero shots.

## Verify

Render with Bevel Radius 0 and then a small value: a highlight line appears on edges only in the second. The AO output darkens crevices only.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch, docs.blender.org manual en/5.2). Confirmed against input/ao and input/bevel: output names Color and AO, inputs, Samples/Inside/Only Local, Cycles-only status and invalid-result cases, Bevel Radius/Normal/Samples (default 4) and cost note. Removed the unsupported EEVEE claim, the 16-sample default, the 0.005 m radius and the scale remark.

Method: documentation only; no commands were run.
