---
id: creative-arts.animation.blender.rocks-cliffs
name: rocks-cliffs
category: creative-arts
field: animation
product: blender
tags: [blender, rocks, cliffs, rock-generator, environment-modeling, displace-modifier, triplanar]
level: practitioner
status: docs-checked
description: "Rocks and cliffs in Blender: layered Displace on evenly dense meshes, modular cliff chunks, Box-projection textures."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/displace.html
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/textures/image.html
  - https://docs.blender.org/manual/en/latest/render/eevee/limitations/nodes_support.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# rocks-cliffs

Goal: believable rock forms quickly, with materials that do not stretch.

## Procedural rock

1. Start from a cube or icosphere and get even density (Remesh or subdivision) before displacing; displacing a low-density mesh gives spikes.
2. Add a Displace modifier with a large-scale texture for big faceted planes. Set *Direction* (Normal displaces along vertex normals), *Midlevel* (the texture value treated as no displacement) and *Strength* (multiplies the offset; negative inverts). A vertex group can limit the effect.
3. Add a second Displace with a smaller-scale texture for breakup. The *Coordinates* option chooses the texture coordinate system used for each vertex.
4. Vary texture offsets to make a family of rocks; apply the modifiers and save variants as assets.
5. Optionally reduce polygon count with Decimate for game assets (`creative-arts.animation.blender.lod-generation`).

## Hero rock

Start from the procedural rock and sculpt planar cuts, flattening and creases by hand with the sculpt brushes, then retopologise or decimate and bake details (`creative-arts.animation.blender.bake-cage`).

## Cliffs

Use a subdivided plane or a blocked-out upright mesh and displace with layered textures along the Normal direction. Build large cliffs from several modular chunks (instanced, rotated, scaled) rather than one giant mesh.

## Materials without stretching

On the Image Texture node set *Projection* to **Box**: it places the image on each side of a unit cube and projects along the axis closest to the mesh normal, so it needs no UVs. *Blend* projects onto multiple sides and blends them; higher values give smoother transitions. Use Object texture coordinates so the mapping follows the object. Moss or dirt masks can be driven by slope (normal against up) and an AO node mask.

## Gotchas

- Non-uniform object scale stretches textures that use object coordinates; apply scale first.
- In EEVEE, Image Texture Box projection with Extend set to Clip or Extend is not supported and always uses Repeat.
- Identical repeated rocks are obvious; rotate, scale and mix variants.

## Checked

2026-11-09. Confirmed against the Displace modifier and Image Texture node manual pages: Direction options, Midlevel, Strength and negative strength, vertex group masking, Coordinates, Box projection and Blend behaviour, and the EEVEE Supported Nodes note on Box projection Extend. Removed: numeric strengths, voronoi and Musgrave texture recipes, Weighted Normal advice, Blend 0.2-0.3, the 4-5 variant count, sculpt tool names, Pointiness advice (sculpt tools page was a stub, not read).
Method: documentation only; no commands were run.

## Verify

Rocks read from several angles with no stretched texture areas; box-projection seams are invisible at shot distance; polygon count is within budget.
