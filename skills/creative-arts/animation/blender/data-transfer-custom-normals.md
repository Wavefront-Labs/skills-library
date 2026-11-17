---
id: creative-arts.animation.blender.data-transfer-custom-normals
name: data-transfer-custom-normals
category: creative-arts
field: animation
product: blender
tags: [blender, data-transfer-custom-normals, transfer-normals, data-transfer, custom-normals, seamless-normals, foliage-normals]
level: practitioner
status: docs-checked
description: "Transfer custom split normals with Blender's Data Transfer modifier: face corner mapping modes, Mix Mode and Factor, vertex group masking, Object Transform and Max Distance."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/modify/data_transfer.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/normals/normal_edit.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# data-transfer-custom-normals

Goal: copy shading normals from another surface, for example to hide seams between separate parts or soften foliage. General Data Transfer usage is in `data-transfer-modifier`; for the stylized cel-face workflow see `cel-shading`.

## Setup

1. On the target object add *Data Transfer* and set **Source** to the mesh to copy from.
2. If the two meshes do not overlap in world space, uncheck **Object Transform** (the axes icon beside Source); the modifier then acts as if both were at the same position with default rotation and scale.
3. In Data Types enable the face-corner type **Custom Normals**.
4. Pick a **Mapping** for face corner data. One-to-one options: *Nearest Corner and Best Matching Normal* (nearest source corner with the most similar split normal), *Nearest Corner and Best Matching Face Normal*, *Nearest Corner of Nearest Face*. Interpolated options: *Nearest Face Interpolated* and *Projected Face Interpolated* (projects the corner along its normal onto a source face and interpolates).
5. **Mix Mode** (Replace, Above/Below Threshold, Mix, Add, Subtract, Multiply) and **Mix Factor** control how much replaces the original; with the threshold modes the factor is a threshold. A **Vertex Group** (+ Invert) gives per-element control of the factor, so only a seam strip can be affected.
6. **Max Distance** (Topology Mapping panel) excludes element pairs further apart than the value; **Ray Radius** is the starting radius for ray-cast matching (low for dense sources, higher for simple ones).

If layers needed for the data type are missing on the target, use **Generate Data Layers**.

## Related

The Normal Edit modifier generates radial or directional custom normals parametrically (for example foliage shading) and can be combined with transfers. The Weighted Normal modifier covers other shading effects.

## Verify

Inspect the seam under changing light or a glossy matcap: no visible crease.

## Checked

Date: 2026-10-27. Documentation release: Blender manual, 5.2 release branch (Data Transfer and Normal Edit pages). Confirmed: option and mapping names, Mix Mode list, Object Transform behaviour, Max Distance, Ray Radius, Generate Data Layers. Removed unconfirmed version gate, stack placement, export-format and baking advice.Method: documentation only; no commands were run.
