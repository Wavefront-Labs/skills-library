---
id: creative-arts.animation.blender.musgrave-fractal
name: musgrave-fractal
category: creative-arts
field: animation
product: blender
tags: [blender, procedural-texturing, musgrave-fractal, musgrave, fractal-noise, ridged-multifractal, hetero-terrain]
level: practitioner
status: docs-checked
description: "Get Musgrave-style fractal noise in Blender 4.1+ via Noise Texture types: fBM, multifractal, hybrid, ridged multifractal, hetero terrain, offset and gain."
sources:
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/textures/noise.html
  - https://developer.blender.org/docs/release_notes/4.1/nodes_physics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# musgrave-fractal

## Musgrave removed

The 4.1 release notes state the Musgrave Texture node was replaced by an extended **Noise Texture** node; the fractal types are now the Noise Texture **Type** dropdown.

## Types (Noise Texture > Type)

- **fBM**: fractal Brownian motion, homogeneous and isotropic; octave values are added.
- **Multifractal**: more uneven, varying by location like real terrain; octave values are multiplied.
- **Hybrid Multifractal**: peaks and valleys with different roughness, like mountains rising from plains; combines addition and multiplication.
- **Ridged Multifractal**: sharp peaks; takes the absolute value of the noise (canyons) and flips the surface upside down.
- **Hetero Terrain**: like Hybrid Multifractal but with the likeness of river channels.

## Inputs

Vector, W, Scale, Detail, Roughness, Lacunarity, Offset (added to each octave; sets where the highest octave appears), Gain (extra multiplier on octave magnitude), Distortion. Inputs are dynamic and appear as the type and dimension need them. Dimensions 1D to 4D.

## Recipes

- Mountain height map for displacement or Geometry Nodes: Ridged Multifractal -> Map Range into the height range you need.
- Marble veins: Ridged Multifractal with some Distortion -> Color Ramp.

## Gotchas

- **Normalize** applies to fBM only; other types need their own remapping (Map Range).
- Compare results against old renders when upgrading files that used the Musgrave node.

## Verify

Switch Type between fBM and Ridged on the same inputs: ridged shows sharp crests.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch, docs.blender.org manual en/5.2). Confirmed against textures/noise (type definitions, Offset, Gain, Normalize on fBM only, dynamic inputs) and the 4.1 Nodes and Physics release notes (Musgrave replaced by an extended Noise Texture). Removed the automatic-conversion and Normalize-off range-matching claims and the numeric recipe values.

Method: documentation only; no commands were run.
