---
id: creative-arts.animation.blender.hair-clump-noise
name: hair-clump-noise
category: creative-arts
field: animation
product: blender
tags: [blender, hair, hair-curves, hair-clump-noise, clump-hair, curl-hair, frizz-hair]
level: practitioner
status: docs-checked
description: "Style Blender Curves hair with the Clump, Curl, Frizz and Hair Curves Noise nodes: factor, shape, guide map, tip spread, frequency and seed inputs."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/hair/guides/clump_hair_curves.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/hair/guides/curl_hair_curves.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/hair/deformation/frizz_hair_curves.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/hair/deformation/hair_curves_noise.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/hair/guides/create_guide_index_map.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# hair-clump-noise

Hair Nodes that shape grooms: **Clump Hair Curves**, **Curl Hair Curves** (Guides category) and **Frizz Hair Curves**, **Hair Curves Noise** (Deformation category).

## Clump Hair Curves
Gathers nearby curves around guide curves. Inputs: **Factor** (0 none, 1 fully pulled to guides), **Shape** (0 constant strength, 0.5 linear falloff root to tip), **Tip Spread**, **Clump Offset**, **Distance Falloff** (0 disables), **Distance Threshold** (maximum distance from a guide), **Seed**, **Preserve Length**. Guide Map group: **Guide Index** (overrides the guide_curve_index attribute), **Guide Distance** (larger gives fewer, bigger clumps), **Guide Mask**, **Existing Guide Map**. Outputs Geometry and the Guide Index used.

## Curl Hair Curves
Wraps curves around nearby guides into curls. Inputs: **Factor**, **Subdivision**, **Curl Start** (percentage along the curve where curling begins), **Radius**, **Factor Start**, **Factor End** (taper the radius), **Frequency** (rotations along the curve, can vary per point), **Random Offset**, **Seed**, plus the same Guide Map group as Clump.

## Frizz Hair Curves
Small random displacements. Inputs: **Cumulative Offset**, **Factor**, **Distance** (displacement magnitude), **Shape** (0 constant, 0.5 linear falloff), **Seed**, **Preserve Length**. Outputs Geometry and an Offset Vector field.

## Hair Curves Noise
Noise-based deformation (waves, turbulence). Inputs: **Cumulative Offset**, **Factor**, **Distance**, **Shape**, **Scale** (noise scale from root position; smaller gives larger waves), **Scale along Curve**, **Offset per Curve**, **Seed**, **Preserve Length**. Outputs Geometry and Offset Vector.

## Guide maps
Create a guide map once with **Create Guide Index Map** (writes the guide_curve_index attribute) and feed it to several nodes so clump, curl and braid agree on guide groups; otherwise each node builds its own from Guide Distance and Guide Mask.

## Gotchas
- A Factor of 0 disables each effect; Distance Falloff 0 makes all nearby curves equally affected by a guide.
- Preserve Length off lets curves stretch or shrink as they are deformed.
- Mask effects with a selection field when only part of the hair should frizz or curl.

## Verify
Toggle each node: clumps, curls, frizz and noise each change the groom in the way their inputs describe.

## Checked

2026-10-27, Blender 5.2 manual (projects.blender.org blender-manual, branch blender-v5.2-release RST) and Python API docs. Compared every input name and meaning with the four node pages. Corrected: Max Distance is Distance Threshold; Shape 0.5 is a linear falloff (not a tip-clumping scale); Curl has Curl Start, Factor Start/End and Subdivision; Frizz has Cumulative Offset and Distance (no Distribution or Random Factor); the noise node is Hair Curves Noise with Scale along Curve and Offset per Curve (no Detail or Distortion). Removed the stack-order advice and photo-based verification.
Method: documentation only; no commands were run.
