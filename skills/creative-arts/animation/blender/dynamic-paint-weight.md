---
id: creative-arts.animation.blender.dynamic-paint-weight
name: dynamic-paint-weight
category: creative-arts
field: animation
product: blender
tags: [blender, dynamic-paint, dynamic-paint-weight, dp-weight, vertex-groups]
level: practitioner
status: docs-checked
description: "Use Blender Dynamic Paint weight surfaces to write vertex groups over time and drive particles and modifiers from contact."
sources:
  - https://docs.blender.org/manual/en/latest/physics/dynamic_paint/canvas.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# dynamic-paint-weight

## Canvas

Surface Type **Weight**, Format Vertex only. Output panel: pick the **Vertex Group** that receives the painted weight (a red name means it does not exist yet; the `+` button creates it; the default name is `dp_weight`).

## Driving effects with the group

- Particle system *Density* vertex group = painted group: particles emit only where the group has weight.
- Any modifier with a *Vertex Group* field (for example Displace or Mask) can read the group.
- Weight surfaces work best with proximity-based brushes so the weight falls off smoothly.

## Settings

- *Dissolve* with *Time* (and *Slow*) fades the weight back to its original state.
- The Effects panel (Spread, Drip, Shrink) is only available on Paint surfaces, not Weight surfaces.

## Recipe: object leaves a fading trail

Weight surface + Dissolve Time 100 frames; the group drives a modifier such as Displace or Mask through its *Vertex Group* field.

## Gotchas

- Weights only exist on vertices; low-poly canvas = coarse result.
- Weight surfaces use Vertex format, which needs a highly subdivided mesh.

## Verify

Weight Paint mode view of the group on several frames shows growth where the brush passed.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (physics/dynamic_paint pages, branch blender-v5.2-release) and the 5.2 source (rna_dynamicpaint.cc, dynamicpaint.cc, properties_physics_dynamicpaint.py). Confirmed: Weight surface is Vertex-format only and outputs a vertex group (manual); Output panel vertex group picker and `+` button, default name dp_weight; Dissolve Time/Slow; Effects panel restricted to Paint surfaces (5.2 UI source); proximity-brush tip.

Method: documentation only; no commands were run.
