---
id: creative-arts.animation.pipeline.scene-units-axes
name: scene-units-axes
category: creative-arts
field: animation
product: pipeline
tags: [scene-units, interchange-formats, up-axis, meters-per-unit, scale-mismatch, frame-rate-conventions, y-up, z-up, pipeline-conventions]
level: practitioner
status: draft
description: "Set and enforce scene unit, up-axis and frame-rate conventions across DCCs so assets and caches move between apps without 100x scale, rotation or timing errors."
sources:
  - https://openusd.org/release/api/group___usd_geom_linear_units__group.html
  - https://docs.blender.org/manual/en/latest/scene_layout/scene/properties.html#units
  - https://help.autodesk.com/view/MAYAUL/2025/ENU/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Units, axes and frame-rate conventions

**Goal:** one written convention for the show, enforced by tools, so nothing arrives 100x too big, lying on
its side, or playing at the wrong speed.

## Defaults by app

| App | Default linear unit | Up axis |
|---|---|---|
| Maya | centimetre | Y |
| Blender | metre | Z |
| Houdini | metre (unitless, 1 unit = 1 m by convention) | Y |
| Unreal | centimetre | Z |
| Unity | metre | Y |
| USD | `metersPerUnit` metadata (0.01 = cm) | `upAxis` metadata (Y or Z) |

## Write the convention

Example show bible entry: "1 unit = 1 cm; Y-up; 24 fps; shots start at 1001 with 8-frame handles; character
height reference 170 units; all publishes record units/axis metadata."

## Enforce

- Scene templates per DCC set units, axis and fps.
- Publish validators (`creative-arts.animation.scripting.pyblish-publish-plugins`) check scene settings and
  bounding box sanity (a character taller than 10 m or smaller than 10 cm fails).
- USD layers carry `metersPerUnit`/`upAxis`; check and convert on import rather than scaling by hand.
- Exporters: set unit conversion explicitly (FBX "Units", Blender "Apply Scalings", Alembic is unitless: the
  receiving side must know).

## Frame-rate conventions

- One show rate (24 or 25 or 23.976); never mix in caches. Time-based formats (USD timecodes, Alembic time
  samples) store time or timecodes; a 24 fps cache read in a 25 fps scene drifts.
- Start frame 1001 convention keeps negative or zero frames out of caches and allows pre-roll.

## Gotchas

- Rotating Z-up to Y-up adds a -90 X rotation at the root; bake it into the asset transforms only once, at
  the boundary.
- Lights and physics are unit-sensitive (light falloff, sim scale); a cm scene with metre-based sim
  settings behaves wrongly.

## Verify

Round trip a reference asset (a 170-unit character cube) through every DCC and back: same size, orientation
and animation timing at frames 1001 and 1120.
