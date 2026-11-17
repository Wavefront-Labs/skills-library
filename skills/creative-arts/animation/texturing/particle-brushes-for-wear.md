---
id: creative-arts.animation.texturing.particle-brushes-for-wear
name: particle-brushes-for-wear
category: creative-arts
field: animation
product: texturing
tags: [particle-brush, painter, wear, hand-painted-detail, substance-painter, grime, texturing]
level: practitioner
status: draft
description: "Paint wear and grime with Painter particle brushes: how particle brushes behave, key settings, masks on fill layers, edge wear, and when to prefer generators."
sources:
  - https://helpx.adobe.com/substance-3d-painter
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Particle brushes for wear

Substance 3D Painter's **particle brushes** paint by simulating many small particles thrown or dropped on the model surface. They produce natural-looking scratches, chips, dust, splatter and drips that a hand brush or generator does not.

## How they work
- The brush emits particles with physical behaviour (such as gravity and bounce), so they interact with surface shapes and settle in crevices and on edges.
- You choose the **particle shape** (an alpha), and settings such as **size** and size jitter, **flow**, **spray** (spread) and **gravity**/**direction**, and rate. Names and options vary by Painter version; see the Painter tools documentation.
- Particles paint the channels you select (colour, roughness, height, and so on), so wear can affect more than albedo.

## Using them for wear
1. Prepare the base (smart materials with generators for general edge wear: `painter-generators.md`, `painter-smart-masks.md`).
2. Add a **fill layer** with the wear material (for example bare metal under paint) and a **black mask**.
3. In the mask, paint with a particle brush to reveal the wear exactly where you want it: scratches near handles, chips on corners, drips under joints.
4. Choose particle alphas that match the material: sharp chips for paint, long thin ones for scratches, soft ones for dust.
5. Vary size and jitter, and paint over several passes; use the eraser to remove strays.

## When to prefer generators
- Large assets and many assets: generators and smart masks are repeatable and fast.
- Particle painting is for hero assets and focal areas where art direction matters.

## Gotchas
- Strokes depend on the model's surface and the camera: check on a fixed lighting setup and from several angles.
- Overdoing wear flattens the material hierarchy; keep wear logical (where it would really occur).

## Verify
- [ ] Wear follows plausible contact and edge areas.
- [ ] Masks are kept (non-destructive) so wear can be adjusted later.
