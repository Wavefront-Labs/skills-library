---
id: creative-arts.animation.blender.procedural-rust-wear
name: procedural-rust-wear
category: creative-arts
field: animation
product: blender
tags: [blender, procedural-texturing, procedural-rust-wear, procedural-rust, edge-wear, grunge]
level: practitioner
status: docs-checked
description: "Procedural rust, edge wear and grunge in Blender: AO-node masks, Pointiness, noise breakup, layered paint, metal and rust."
sources:
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/input/ao.html
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/input/geometry.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# procedural-rust-wear

## Masks

- **Edge wear:** the Ambient Occlusion node with **Inside** enabled detects convex rather than concave shapes by computing occlusion inside the mesh. Its **Distance** sets how far other geometry counts as occluding; a short distance keeps the mask tight to edges. Feed the AO factor output through a Color Ramp to shape it. Pointiness from the Geometry node is an alternative (Cycles only, and it needs dense enough geometry to vary).
- **Crevice dirt and rust:** the AO node with Inside off detects concave shapes; invert or ramp it.
- **Breakup:** multiply the mask by a noise texture, then ramp, to get patchy, chipped edges rather than uniform lines. Tune scale and detail by eye.
- **Drips:** stretch a noise along the vertical axis (via the Mapping node) and multiply it by a height gradient.

## Layers

1. Base paint on a Principled BSDF.
2. Bare metal where the edge-wear mask is high (raise Metallic, lower Roughness).
3. Rust where the crevice or patch mask is high: orange to dark-brown colour ramp, high roughness, no metallic, and a bump from noise.

Combine the layers by mixing colour and value inputs with the masks into one Principled BSDF.

## Gotchas

- The AO node is expensive in Cycles and can slow renders significantly. The manual suggests using Pointiness or baking Ambient Occlusion for faster renders. The AO node's *Samples* should be kept as low as possible.
- Pointiness and the AO node's Only Local option are Cycles-only.
- Uniform rust everywhere looks fake; drive coverage by masks and story (water pools, contact points).

## Checked

2026-11-09. Confirmed against the Ambient Occlusion node and Geometry node manual pages: Inside (convex), Distance, Samples, Cycles cost, bake or Pointiness advice, Pointiness Cycles-only. Removed: numeric values (distance, noise settings, colours, roughness), the Bevel-node edge trick, Mix node names, and the studio training page (not read).
Method: documentation only; no commands were run.

## Verify

Rust in recesses and drips below them; chipped edges only on exposed convex edges.
