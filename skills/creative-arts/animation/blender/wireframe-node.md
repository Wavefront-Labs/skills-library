---
id: creative-arts.animation.blender.wireframe-node
name: wireframe-node
category: creative-arts
field: animation
product: blender
tags: [blender, shader, wireframe-node, wireframe-shader, edges-render]
level: practitioner
status: docs-checked
description: "Render mesh edges with the Blender Wireframe shader node: size, pixel size, triangulation caveat, and alternatives with the Wireframe modifier."
sources:
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/input/wireframe.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# wireframe-node

## Wireframe node

- Retrieves the edges of an object as they appear to Cycles. Output **Factor**: a black-and-white mask with white lines on edges. Inputs: none. Properties: **Size** (thickness of the edge lines) and **Pixel Size** (when enabled, the size is set in screen space).
- Mix Shader Fac = Wireframe -> edge material on top of the base (tech showcase, holograms).

## Caveat

Meshes are triangulated before Cycles processes them, so topology always appears triangulated: diagonal edges inside quads show. Workarounds:
- **Wireframe modifier** (real geometry from the mesh edges) on a duplicate with an emissive material.
- Freestyle or Line Art for clean edges in stylised renders.
- Geometry Nodes: Mesh to Curve -> Curve to Mesh for tubes along edges.

## Recipes

- Clay and wire turntable: white diffuse base; Wireframe with Pixel Size -> Mix to a dark grey.
- Hologram: Wireframe Factor -> Emission Strength with Layer Weight Facing.

## Verify

Render close and far shots with Pixel Size on: line width stays constant; triangle diagonals show on quads unless using the modifier approach.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch, docs.blender.org manual en/5.2). Confirmed against input/wireframe: Factor output, Size and Pixel Size, triangulation caveat. Removed the unconfirmed EEVEE antialiasing and 2 px advice, the render-subdivision remark and the claim that the Wireframe modifier gives quad edges only.

Method: documentation only; no commands were run.
