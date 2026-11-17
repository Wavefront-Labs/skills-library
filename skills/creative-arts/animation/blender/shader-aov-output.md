---
id: creative-arts.animation.blender.shader-aov-output
name: shader-aov-output
category: creative-arts
field: animation
product: blender
tags: [blender, aov, aov-shader-output, aov-output, shader-aov, render-passes]
level: practitioner
status: docs-checked
description: "Create custom render passes with Shader AOVs: register AOVs on the view layer, AOV Output node in materials, colour vs value types, and uses like masks and IDs."
sources:
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/output/aov.html
  - https://docs.blender.org/manual/en/5.2/render/layers/passes.html
  - https://docs.blender.org/api/current/bpy.types.AOV.html
  - https://docs.blender.org/api/current/bpy.types.AOVs.html
  - https://docs.blender.org/api/current/bpy.types.ShaderNodeOutputAOV.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# shader-aov-output

Goal: write any shader value (mask, ID, texture, fresnel, custom lighting term) into its own render pass.

## Two parts

1. View Layer Properties > **Shader AOV** panel: add a pass, give it a **Name** (for example `rim_mask`) and a Data Type: **Color** (a colour, normal or other vector) or **Value** (a single number).
2. In each material that should write to it: add an **AOV Output** node (Output category), set its **Name** to the same string and connect **Color** or **Value**. The node can also be used in World shader nodes.

The pass is read in the compositor from the socket on the Render Layers node. The pass name is used in both the AOV Output node and the Render Layers node and must not conflict with other enabled passes.

## Limits

- At most 16 Color and 16 Value AOVs.
- Transparent materials using the EEVEE Blended render method are not rendered in passes other than Combined and Transparent; use Dithered.

## Uses

- Masks: dirt, wetness or damage areas, for grading only those parts.
- IDs that Cryptomatte cannot give: a texture-driven region or UV-based zones.
- Debug or fine-tune very small details in post-processing.

## Python

```python
vl = bpy.context.view_layer
aov = vl.aovs.add(); aov.name = "rim_mask"; aov.type = "VALUE"
node = mat.node_tree.nodes.new("ShaderNodeOutputAOV"); node.aov_name = "rim_mask"
```

## Gotchas

- The node's Name must match the Shader AOV name exactly; copy and paste it.

## Verify

View the AOV pass in the compositor Viewer. Only the intended materials should have values.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch, docs.blender.org manual en/5.2). Confirmed against output/aov, the Shader AOV section of the render passes page (panel, Name, Data Type Color/Value, Render Layers socket, 16+16 limit, Blended limitation) and the Python API pages for AOV (name, type COLOR/VALUE), AOVs.add() and ShaderNodeOutputAOV.aov_name. Removed the unconfirmed claims about missing nodes writing 0, multilayer EXR, antialiasing and transparency behaviour.

Method: documentation only; no commands were run.
