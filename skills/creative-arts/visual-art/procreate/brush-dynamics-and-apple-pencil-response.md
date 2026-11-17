---
id: creative-arts.visual-art.procreate.brush-dynamics-and-apple-pencil-response
name: brush-dynamics-and-apple-pencil-response
category: creative-arts
field: visual-art
product: procreate
tags: [visual-art, procreate, brush-dynamics, stroke-path, apple-pencil, brush-studio, tilt, pressure-response, procreate-dynamics]
level: advanced
status: draft
description: "Edit Procreate brush stroke path, dynamics and Apple Pencil response in Brush Studio so a brush reacts to pressure, tilt and speed the way you want."
sources: ["https://procreate.com/handbook"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stroke path, dynamics and Apple Pencil settings in Brush Studio

**Goal:** make a brush respond predictably. Open Brush Studio by tapping a brush in the Brush Library. Panels (Handbook, Brush Studio): Stroke path, Stabilization, Taper, Shape, Grain, Rendering, Wet mix, Color dynamics, Dynamics, Apple Pencil, Properties, About this brush. Names can shift between versions.

## Stroke path
- **Spacing:** distance between stamps of the brush shape; low spacing gives a continuous line, higher gives dotted or textured marks.
- **Jitter:** random offset of stamps off the path; **Fall off** fades the stroke over distance.
- Duplicate the brush before editing so the original stays intact (swipe left > Duplicate).

## Dynamics
- Speed-based changes (size or opacity varying with how fast you draw) and jitter amounts live here; use for ink brushes that thin out when drawn quickly.

## Apple Pencil panel
- **Pressure:** mapping of pressure to size and opacity via curves; flatten them for a uniform line, steepen for expressive tapering.
- **Tilt:** with the Pencil on its side, shading-style behaviour (opacity, size, bleed or shape) for pencil and chalk brushes.
- **Bleed and flow** options reproduce soft build-up when pressing.
- Edit each curve by dragging its points, and test in the drawing pad at the bottom of the Brush Studio screen.

## Gotchas
- Global pressure settings (Prefs) combine with brush curves; if a brush feels twice as sensitive as expected, check both (`creative-arts.visual-art.procreate.pressure-curve-and-smoothing-settings`).
- Finger painting reports no pressure or tilt, so those curves appear dead.
- Do not edit the stock brush in place if you want to reset later; duplicate first.

## Verify
- [ ] The drawing pad shows the expected range from light to heavy marks.
- [ ] Tilting the Pencil changes the mark in the way set in the Tilt curve.
