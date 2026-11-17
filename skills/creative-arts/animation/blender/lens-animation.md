---
id: creative-arts.animation.blender.lens-animation
name: lens-animation
category: creative-arts
field: animation
product: blender
tags: [blender, camera-animation, lens-animation, dolly-zoom, zoom, focal-length, vertigo-effect, drivers]
level: practitioner
status: docs-checked
description: "Animate camera focal length in Blender: smooth zooms, crash zooms, and a driver-based dolly zoom (vertigo effect) that keeps the subject's size constant while the background warps."
sources:
  - https://docs.blender.org/manual/en/latest/render/cameras.html#lens
  - https://docs.blender.org/manual/en/latest/animation/drivers/drivers_panel.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# lens-animation

## Zooms

- Camera data > **Focal Length**: hover and I to key. Zoom ease-in/out in the Graph Editor; crash zooms: a few frames with strong easing.
- The manual defines longer focal lengths as a smaller field of view (more zoom); it suggests decreasing Focal Length while the camera moves toward an object for a Dolly Zoom, or the reverse.
- Sensor width matters for real-camera matching (see `camera-sensor-fit`).

## Dolly zoom (vertigo) with a driver

Subject width on screen ∝ focal_length / distance. Keep it constant: `focal = k × distance`.
1. Empty `subject` at the subject. Camera aimed at it (Track To).
2. Animate only the camera's translation along its view axis (toward/away).
3. Driver on Focal Length: a **Distance** variable `d` (the distance between two objects or bones) from camera to `subject`; expression `d * k` where `k = initial_focal / initial_distance` (e.g. 35 mm at 5 m → k = 7).
4. Scrub: subject stays the same size; background perspective warps.

## Gotchas

- Very short focal lengths from the driver near the subject distort heavily; limit the move range or clamp in the expression (`clamp` is among the driver expression functions; `clamp(d*7, 18, 200)`).
- Set the camera's DOF **Focus on Object** to the subject during a dolly zoom.

## Verify

Overlay a guide (composition guides, or a reference empty) — the subject's silhouette width is constant through the move.

## Checked
2026-10-27, Blender 5.2 manual (blender-v5.2-release RST), render/cameras (Focal Length hint, Dolly Zoom) and animation/drivers/drivers_panel (Distance variable type, clamp in expression functions). The k = focal / distance relation is geometry, not a manual claim. Removed unconfirmed crash-zoom timing and FBX bake claims.
Method: documentation only; no commands were run.
