---
id: creative-arts.animation.blender.dynamic-paint-brush
name: dynamic-paint-brush
category: creative-arts
field: animation
product: blender
tags: [blender, dynamic-paint, dynamic-paint-brush, dp-brush, paint-source]
level: practitioner
status: docs-checked
description: "Configure Blender Dynamic Paint brushes: paint colour and alpha, source types (mesh volume, proximity, particles), velocity and wave settings."
sources:
  - https://docs.blender.org/manual/en/latest/physics/dynamic_paint/brush.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# dynamic-paint-brush

## Setup

Physics > Dynamic Paint > Type **Brush**.

## Settings

- **Paint**: Paint Color, Alpha, **Absolute Alpha**, **Erase Paint**, **Wetness**.
- **Source** (the *Paint* menu in the Source panel):
  - **Mesh Volume**: paints every canvas point inside the brush mesh volume.
  - **Proximity**: paints within *Distance* of the brush surface; *Falloff* (Smooth, Constant, Color Ramp); **Project** with a *Ray Direction* (Canvas Normal, Brush Normal, Z-Axis).
  - **Mesh Volume + Proximity**: both, with *Inner Proximity* and *Negate Volume*.
  - **Object Center**: distance to the object origin only (faster than mesh proximity); *Distance* and *Falloff* apply.
  - **Particle System**: each particle paints; *Effect Solid Radius* (or *Use Particle's Radius*) plus *Smooth Radius*.
- **Velocity** panel: *Multiply Alpha*, *Replace Color*, *Multiply Depth* via a colour ramp from zero to *Max Velocity* (units per frame), and *Do Smudge* with *Smudge Strength*.
- **Waves** (for wave canvases): Type (Depth Change, Obstacle, Force, Reflect Only), Factor, Clamp.

## Recipes

- Footprints in sand: foot = brush, Mesh Volume + Proximity, Distance 0.02; canvas Displace (dynamic-paint-displace).
- Rain spots: particle system brush with a small Effect Solid Radius.

## Gotchas

- Brush must actually intersect/come close to the canvas; check scale.
- Distance is in Blender units.
- Brush on many objects: use the canvas surface's *Brush Collection* to limit which objects act as brushes.

## Verify

The canvas colour attribute (Vertex format) or the baked image sequence shows paint where contact happened.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (physics/dynamic_paint pages, branch blender-v5.2-release) and the 5.2 source (rna_dynamicpaint.cc, dynamicpaint.cc, properties_physics_dynamicpaint.py). Confirmed: brush Paint Color/Alpha/Wetness/Absolute Alpha/Erase Paint; every Source option and its sub-settings (Distance and Falloff shown only for Proximity, Mesh Volume + Proximity and Object Center); Project Ray Direction enum; Velocity panel options and units; Brush Collection on the canvas surface.

Method: documentation only; no commands were run.
