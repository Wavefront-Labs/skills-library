---
id: creative-arts.animation.texturing.painter-generators
name: painter-generators
category: creative-arts
field: animation
product: texturing
tags: [generators, painter-layers, substance-painter, mask-generator, dirt-generator, edge-wear, curvature, ambient-occlusion, mesh-maps, procedural-masks]
level: practitioner
status: draft
description: "Drive masks procedurally with Substance 3D Painter generators (dirt, metal edge wear, mask builder) from baked mesh maps; tuning levels, grunge and global balance."
sources:
  - https://helpx.adobe.com/substance-3d-painter/painting/masking-and-effects/generator.html
  - https://helpx.adobe.com/substance-3d-painter/painting/masking-and-effects.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Generators

**Goal:** masks that place wear, dirt and highlights where they would naturally occur (edges, cavities,
upward faces), computed from baked mesh maps and updated automatically when the mesh changes.

## Using a generator

1. Add a black mask to a fill layer (right-click - Add black mask).
2. Right-click the mask - Add generator; choose one:
   - **Metal Edge Wear**: convex edges from curvature (paint chipping off).
   - **Dirt**: cavities and occluded areas from AO and curvature.
   - **Mask Builder**: combines AO, curvature, position gradient and grunge in one generator; the most
     flexible.
   - **Position / Light**: gradients by world height or a light direction (dust on top, moss on north side).
3. Tune: Global balance/levels first, then contrast, then grunge amount/scale, then each input's weight.

## Layering generators and effects

Masks are stacks too: generator + Levels + Fill (grunge texture) set to Multiply + Paint (manual fixes)
+ Blur. Order matters (top affects result of everything below).

## Requirements

Generators read baked maps: **curvature, ambient occlusion, world space normal, position, thickness**.
Bake them first (`creative-arts.animation.texturing.painter-mesh-map-baking`); bad bakes give wear in
wrong places.

## Stylised animation use

- Edge highlights for cel-like painted look: Metal Edge Wear with low grunge, sharp contrast, coloured
  lighter fill: a painterly edge light baked into texture.
- Keep generator scale consistent across a set's props (shared values in a smart material) so wear reads
  as one world.

## Gotchas

- Generator results depend on texel density and mesh scale; same settings look different on large vs
  small objects. Use world-scale aware options where offered.
- Generators re-compute on resolution change; check after changing export size.

## Verify

Rotate the model under the viewport light: wear sits on exposed edges, dirt in crevices; changing the
mesh (re-import) moves masks with the new geometry without repainting.
