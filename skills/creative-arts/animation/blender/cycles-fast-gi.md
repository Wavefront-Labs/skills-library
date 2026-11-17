---
id: creative-arts.animation.blender.cycles-fast-gi
name: cycles-fast-gi
category: creative-arts
field: animation
product: blender
tags: [blender, cycles, fast-gi, fast-gi-approximation, ambient-occlusion, light-paths]
level: practitioner
status: docs-checked
description: "Use Cycles Fast GI Approximation to replace diffuse indirect light with AO: Replace vs Add methods, viewport/render bounces, AO distance and factor."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/light_paths.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# cycles-fast-gi

Goal: trade some accuracy for speed by approximating diffuse indirect light with background-tinted ambient occlusion.

## Settings (Render Properties > Light Paths > Fast GI Approximation; enable the checkbox)

The manual describes it as a fast alternative to full global illumination, for interactive viewport rendering or final renders with reduced quality.

- **Method**: *Replace* replaces global illumination with ambient occlusion after a specified number of bounces. *Add* adds ambient occlusion to diffuse surfaces.
- **AO Factor**: strength of the ambient occlusion (Python: `world.light_settings.ao_factor`).
- **AO Distance**: distance from the shading point to trace rays (Python: `world.light_settings.distance`). Shorter emphasises nearby features; longer also takes farther objects into account. It can be overridden per object in Object Properties, useful when small and large objects share a scene.
- **Viewport Bounces**: bounces before global illumination is replaced by AO in the 3D viewport. The manual notes this can reduce noise in interior scenes with little visual difference.
- **Render Bounces**: the same for final renders.

## Workflow

1. Render a reference frame with Fast GI off.
2. Enable Fast GI with Replace and a low bounce count, and compare time and the darkest corners.
3. Tune AO Distance to the scale of the set, and AO Factor to match overall brightness.
4. Keep the settings identical across a sequence so shots match.

## Gotchas

- The approximation is background-tinted AO, so the world colour and strength affect the replaced lighting.
- Coloured bounce light from the replaced bounces is approximated, not traced; compare against the reference.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual, Cycles Light Paths (Fast GI Approximation). Confirmed: panel location, Method Replace/Add, AO Factor, AO Distance and per-object override, Viewport/Render Bounces. Removed unconfirmed: percent speed savings, recommended bounce numbers, scene-type failure claims.
Method: documentation only; no commands were run.
