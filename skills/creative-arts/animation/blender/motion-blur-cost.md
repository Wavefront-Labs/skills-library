---
id: creative-arts.animation.blender.motion-blur-cost
name: motion-blur-cost
category: creative-arts
field: animation
product: blender
tags: [blender, render-optimization, motion-blur-cost, motion-blur, shutter-curve, cycles]
level: practitioner
status: docs-checked
description: "Render Cycles motion blur efficiently: shutter, position, rolling shutter and shutter curve, per-object deformation and steps, and documented limits."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/motion_blur.html
  - https://docs.blender.org/manual/en/latest/render/cycles/object_settings/object_data.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# motion-blur-cost

Goal: accurate motion blur in Cycles without wasting memory or time.

## Render Properties > Motion Blur (Cycles)

- **Position**: Start on Frame (shutter starts opening at the current frame), Center on Frame (fully open at the current frame), End on Frame (fully closed at the current frame).
- **Shutter**: time in frames between the shutter starting to open and being fully closed; 1.0 blurs over the length of one frame.
- **Rolling Shutter**: None or Top-Bottom. **Rolling Shutter Duration** balances pure rolling shutter (0) against pure motion blur (1).
- **Shutter Curve**: curve defining how the shutter opens and closes (X is time, Y 0 closed to 1 fully open). The default mapping opens and closes instantly.

If the scene has particles or other physics, bake them before rendering, otherwise motion blur may be incorrect or inconsistent.

## Per object (Object Properties > Motion Blur)

- Motion Blur toggle: applies only to the motion of the object itself; disabling it does not remove blur from camera motion or animated focal length.
- **Deformation**: enables blur for deforming meshes such as animated characters, including hair. Topology that changes over time (animated Booleans, Deformation before Edge Split, Remesh, Skin or Decimate modifiers) cannot render deformation blur correctly, so disable it for those objects.
- **Steps**: accuracy of deformation motion blur; more steps use more memory. The actual number of time steps is 2^(steps - 1).

## Costs

Cost depends on the scene. Measure render time and peak memory with blur on and off, and with Deformation off on rigid objects. More Steps means more memory.

## Limitations (from the manual)

- Camera motion blur does not work for orthographic cameras.
- Motion blur ignores movement of lights in world coordinates, so moving the camera together with lights wrongly produces blur.

## Alternative

Render without blur plus a Vector pass and use the compositor Vector Blur (see comp-vector-blur).

## Verify

Render a fast-moving frame with Steps at two values on the moving object and compare arcs; compare time and memory against the unblurred frame.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (Cycles Motion Blur, Object settings). Confirmed: Position, Shutter, Rolling Shutter, Shutter Curve, Steps formula, Deformation and its warning, limitations. Removed unconfirmed: 180-degree equivalence, step recommendations, 10 to 40 percent time claim, hair/crowd advice, camera-cut gotcha.
Method: documentation only; no commands were run.
