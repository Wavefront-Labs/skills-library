---
id: creative-arts.animation.pipeline.alembic-caches
name: alembic-caches
category: creative-arts
field: animation
product: pipeline
tags: [alembic, interchange-formats, abc, point-cache, geometry-cache, animation-cache, uv-write, face-sets, maya-abc-export, blender-alembic]
level: advanced
status: draft
description: "Export and import Alembic animation caches between departments: what to include (UVs, normals, face sets, attributes), frame ranges, subframes, and naming for re-cache."
sources:
  - https://docs.alembic.io/
  - https://help.autodesk.com/view/MAYAUL/2025/ENU/
  - https://docs.blender.org/manual/en/latest/files/import_export/alembic.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Alembic caches

**Goal:** baked animated geometry handed from animation to FX/lighting that matches the rig's motion exactly,
loads fast, and can be re-cached without breaking downstream shaders.

## What goes in

| Data | Why |
|---|---|
| Deformed mesh positions per frame | the motion |
| UVs (`-uvWrite`) | textures on the cache |
| Normals (`-writeNormals` or let renderer compute) | correct smoothing on hard edges |
| Face sets (`-writeFaceSets`) | per-face material assignment |
| Custom attributes (`-attr`, `-attrPrefix`) | IDs, masks for FX/lighting |
| Visibility (`-writeVisibility`) | hidden props in parts of the shot |
| World space or local (`-worldSpace`) | agree with the receiving department |

## Maya export (MEL/Python AbcExport)

```python
from maya import cmds
cmds.AbcExport(j="-frameRange 1001 1120 -step 1 -frameRelativeSample -0.25 -frameRelativeSample 0 "
                 "-frameRelativeSample 0.25 -uvWrite -writeFaceSets -writeVisibility -worldSpace "
                 "-dataFormat ogawa -root |hero_GRP|geo_GRP -file <SHOT>/cache/hero_anim_v004.abc")
```
- Frame range with **handles** (e.g. 8 frames before and after the cut) for motion blur and FX pre-roll.
- Subframe samples (frameRelativeSample) for motion blur accuracy on fast motion; or let the renderer use
  velocity.
- `-root` the geometry group, not the rig controls.
- Ogawa format (default since Alembic 1.5) is much faster than HDF5.

## Blender

File - Export - Alembic: Frame range, Sub-frame (Transform/Geometry samples), UVs, Normals, Face Sets,
Apply subdivision (usually off; subdivide at render). Import uses a Mesh Sequence Cache modifier that streams.

## Re-cache safety

- Keep the hierarchy and mesh names identical between versions so lighting's shader assignments still match.
- Topology must not change (point count/order) for downstream tools that rely on point IDs.
- Version the cache file (`_v004`), never overwrite a published cache.

## Gotchas

- Point count changing mid-shot (dynamic topology) breaks motion blur from positions; export velocities.
- Scale and up-axis differences between apps (`creative-arts.animation.pipeline.scene-units-axes`).

## Verify

Import the cache in the receiving app, overlay it on a playblast of the rig: frame-matched motion, UVs show a
checker correctly, materials assigned by face set.
