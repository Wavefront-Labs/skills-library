---
id: creative-arts.animation.blender.voronoi-texture
name: voronoi-texture
category: creative-arts
field: animation
product: blender
tags: [blender, procedural-texturing, voronoi-texture, voronoi, cellular, distance-metric]
level: practitioner
status: docs-checked
description: "Use Blender Voronoi Texture features (F1, F2, smooth F1, distance to edge, n-sphere radius), distance metrics, randomness and outputs for cells and cracks."
sources:
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/textures/voronoi.html
  - https://docs.blender.org/api/current/bpy.types.ShaderNodeTexVoronoi.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# voronoi-texture

## Feature modes

- **F1**: distance to the closest feature point, plus its position and colour (cells, spots).
- **F2**: distance to the second closest point; F2 minus F1 (via Math) gives cell borders.
- **Smooth F1**: a smooth version of F1, controlled by Smoothness.
- **Distance to Edge**: distance to the edges of the cells (cracks, grout, cell walls); threshold it with a constant Color Ramp.
- **N-Sphere Radius**: radius of the n-sphere inscribed in the cell (half the distance between the closest feature point and the point nearest to it); gives tightly packed circles.

## Distance metric

Euclidean, Manhattan, Chebychev, Minkowski (generalisation with an **Exponent**: 1 equals Manhattan, 2 equals Euclidean, infinite equals Chebychev; 32 approximates Chebychev).

## Inputs and outputs

- Inputs: Vector, W, Scale, Detail, Roughness, Lacunarity (octave controls), Smoothness, Exponent, Randomness. Inputs are dynamic and appear as the Feature and Dimensions need them. Dimensions 1D to 4D (higher is slower). **Normalize** keeps output in 0 to 1 (rarely outside it for F2).
- Outputs: **Distance**, **Color** (arbitrary per-cell colour), **Position** (feature point position; feed into textures for per-cell sampling), **W**, **Radius**.

## Recipes

- Cobblestones: Smooth F1 for the stone shape plus Distance to Edge for the gaps; Color for per-stone tint.
- Beveled cells: the difference between F1 and Smooth F1.
- Crackle: Distance to Edge through a Color Ramp to thin lines.

## Gotchas

- Rendering artifacts can appear at low Randomness for the same precision reasons described in the White Noise Texture notes in the manual; see its fixes.
- Per-cell Color is arbitrary; remap through a Color Ramp for palette control.

## Verify

Preview Distance to Edge through a constant ramp: crisp thin network lines at the expected spacing.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch, docs.blender.org manual en/5.2). Confirmed against textures/voronoi and the Python API page for ShaderNodeTexVoronoi: features, metrics and Minkowski equivalences, inputs, Normalize, outputs, notes on artifacts. Removed the '4.0+ fractal Voronoi' gate, the Chebychev-for-tiles and scales recipes, the Distance to Edge detail-noise claim and the numeric threshold and exponent shapes.

Method: documentation only; no commands were run.
