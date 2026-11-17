---
id: creative-arts.animation.blender.ant-landscape
name: ant-landscape
category: creative-arts
field: animation
product: blender
tags: [blender, ant-landscape, landscape-addon, terrain, environment-modeling, procedural-terrain, erosion]
level: intro
status: gated
description: "Generate terrain with the A.N.T. Landscape add-on: noise types and settings, subdivisions and size, falloff and edges, Landscape Eroder, displace tools and regenerating."
sources:
  - https://docs.blender.org/manual/en/4.1/addons/add_mesh/ant_landscape.html
  - https://extensions.blender.org/add-ons/antlandscape/
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# ant-landscape

Goal: quick procedural terrain meshes for backgrounds, layout and sculpt starting points.

## Install

The Blender 4.1 manual documents it as a bundled add-on (Add Mesh: A.N.T. Landscape, A.N.T. = Another Noise Tool). The extensions.blender.org listing "A.N.T.Landscape" ("Another Noise Tool: Landscape and Displace") shows a minimum of Blender 4.2, so on current releases install it as an extension. Add the mesh from 3D Viewport → Add → Mesh, or from the Sidebar Create tab.

## Main settings (redo panel or sidebar Create → Landscape)

After creating the landscape the Adjust Last Operation panel has three areas (4.1 manual):

- **Main Settings**: object and mesh settings such as size and subdivisions.
- **Noise Settings**: noise settings that give the terrain its shape; there are many noise types and settings.
- **Displace Settings**: terrain height and edge falloff (the manual also mentions Strata).

The exact property names and noise type list were not confirmed against the current extension. (gated: unconfirmed, source is paywalled or blocked)

## Editing after creation

- The Landscape panel adds panels and tools to the Sidebar: *Landscape Main* (adjust main settings and regenerate the mesh; smooth, triangulate, rename, add materials), *Landscape Noise* and *Landscape Displace* (adjust those settings and refresh only them).
- **Mesh Displace**: displaces selected mesh vertices along the normal or X, Y, Z.
- **Weight from Slope**: generates a weighted vertex group slope map from the Z normal value.
- **Landscape Eroder**: applies various kinds of erosion to an A.N.T. Landscape grid; also available in the Weights menu in Weight Paint Mode.

## Workflow

1. Generate at low subdivisions to find the shape (seed, noise size, height).
2. Increase subdivisions for the final.
3. Optionally use the result as a sculpt base (practice).

## Gotchas

- Face count grows with the square of the subdivisions; keep resolution reasonable (practice).
- Check the terrain scale against a character (practice).

## Verify

Terrain matches the intended scale next to a reference character; the Eroder visibly changes the terrain.

## Checked

2026-10-27, Blender manual 4.1 (add-on docs) and extensions.blender.org. Confirmed against the Blender 4.1 manual page add_mesh/ant_landscape (interface locations, three settings areas, Sidebar tools, Eroder) and the extensions.blender.org listing for A.N.T.Landscape (tagline, minimum Blender 4.2), both fetched on this date. Removed unconfirmed property names, noise type list, Water plane, Falloff options and the million-face figure. The extension's current property names are unconfirmed and gated.

Method: documentation only; no commands were run.
