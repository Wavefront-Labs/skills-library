---
id: creative-arts.animation.blender.dynamic-paint-waves
name: dynamic-paint-waves
category: creative-arts
field: animation
product: blender
tags: [blender, dynamic-paint, dynamic-paint-waves, dp-waves, ripples]
level: practitioner
status: docs-checked
description: "Make water ripples with Blender Dynamic Paint wave canvases: timescale, speed, damping, spring, smoothness, open borders and brush wave types."
sources:
  - https://docs.blender.org/manual/en/latest/physics/dynamic_paint/canvas.html
  - https://docs.blender.org/manual/en/latest/physics/dynamic_paint/brush.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# dynamic-paint-waves

## Canvas

Canvas Surface Type **Waves**. Needs a dense subdivided plane (vertex format) or image sequence.

## Settings

- **Open Borders**: waves pass through mesh edges instead of reflecting.
- **Timescale**: simulation speed without changing the outcome; **Speed**: how fast waves travel (halving it equals a surface twice as large).
- **Damping**: how fast waves die out. **Spring**: force pulling the surface back to zero level. **Smoothness**: limits the maximum slope between simulation points, removing noise from sharp-edged brushes.
- Waves surfaces have no *Dissolve* panel.

## Brush side (Waves panel)

- **Depth Change**: waves appear where the intersection depth changes; a stationary brush has no effect. A negative Factor gives a wake for moving objects such as ships.
- **Obstacle**: constantly affects the surface while intersecting and reflects waves; a stationary brush makes an unnatural dent.
- **Force**: directly affects wave velocity.
- **Reflect Only**: no effect alone but reflects waves already on the surface.
- **Factor** sets how strongly brush depth drives the simulation (negative pulls the surface up); **Clamp Waves** limits the influence depth.

## Recipe: drop into a pond

Plane subdivided to 200×200, canvas Waves, Open Borders, Damping 0.05, Speed 1; falling sphere brush Wave type Depth Change Factor 1.

## Gotchas

- Vertex format needs a highly subdivided mesh, and Vertex-format Waves surfaces have no Output panel. Add Smooth shading.
- Unstable motion around the brush: reduce wave speed, the brush Factor, or the mesh/surface resolution.
- Too low resolution = blocky ripples; raise subdivisions or use image sequence + displacement.

## Verify

Ripples propagate outward and fade; boundaries do not reflect when Open Borders is on.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (physics/dynamic_paint pages, branch blender-v5.2-release) and the 5.2 source (rna_dynamicpaint.cc, dynamicpaint.cc, properties_physics_dynamicpaint.py). Confirmed: Waves canvas settings (Open Borders, Timescale, Speed, Damping, Spring, Smoothness) and their descriptions; the four brush Wave Types, Factor and Clamp Waves; stability tip; Dissolve panel hidden for Waves; no Output panel for Vertex-format Waves.

Method: documentation only; no commands were run.
