---
id: creative-arts.animation.blender.brush-settings-falloff
name: brush-settings-falloff
category: creative-arts
field: animation
product: blender
tags: [blender, sculpting, brush-settings-falloff, brush-falloff, stroke-method, stabilizer, lazy-mouse, pressure, spacing]
level: practitioner
status: docs-checked
description: "Tune Blender brushes: size and strength with pressure, Size Unit view vs scene, falloff presets and curves, stroke methods, dashes and the stabilizer."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/brush/brush_settings.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/brush/falloff.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/brush/stroke.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# brush-settings-falloff

Goal: a brush that behaves predictably (right size, softness and stroke behaviour) in every paint and sculpt mode.

## Basics

- **F** sets Size interactively, **Shift-F** sets Strength, and **Ctrl-F** rotates the texture Angle. `[` and `]` shrink and grow the size. Pressure icons next to Size and Strength use a graphics tablet; each has an optional pressure curve.
- **Size Unit** (Sculpt Mode): *View* measures size in screen space; *Scene* measures in real-world units so the size stays constant while zooming (units come from Scene Units).
- **Direction** (Add/Subtract) toggles with Ctrl in Sculpt Mode.
- The brush icon marked as unified (Use Unified Size, Strength, Color) shares that value across all brushes of the mode without overwriting each brush's own value.

## Falloff

Curve Preset: Custom, or the predefined Smooth, Smoother, Sphere, Root, Sharp, Linear, Sharper, Inverse Square and Constant. In a Custom curve the left side is the brush centre and the right side the edge. **Falloff Shape**: *Sphere* uses 3D world distance; *Projected* uses a 2D screen-space circle, so nearby-looking points on the screen are affected regardless of their distance in the world (Texture Paint always uses Projected). Hardness (Sculpt Mode) sets how close to the edge the falloff starts.

## Stroke methods (Stroke panel, Alt-E)

- **Dots**: a dab on every mouse move, so slower strokes accumulate more strength.
- **Drag Dot**: one dab that you place by dragging.
- **Space**: dabs separated by **Spacing**, a percentage of the brush radius.
- **Airbrush**: continuous while held, at the **Rate** interval.
- **Anchored**: a single dab; click and drag to resize it. **Edge to Edge** defines it by two opposite points.
- **Line**: drag a screen-space line; dabs are separated by Spacing; hold Alt for 45 degree steps.
- **Curve**: strokes follow a Paint Curve data-block. Ctrl-RMB adds points (the first one creates the curve), drag to set handles, X deletes a point, Return or the Draw Curve button runs the stroke.
- Also: **Spacing Distance** (View or Scene, Sculpt Mode), **Adjust Strength for Spacing** (Space, Line, Curve), **Dash Ratio** and **Dash Length** (Space, Line, Curve; useful for stitches), **Jitter** with a View or Scene unit, and **Input Samples** (averages recent mouse positions).

## Stabilize Stroke

Enable with Shift-S or the header checkbox. **Radius** is the minimum distance from the last point before the stroke continues; **Factor** is a smoothing amount where higher values smooth more but feel like pulling the stroke.

## Brush assets

Changes to a brush asset's settings are temporary and discarded when Blender closes. Keep them with Save Changes to Asset, or make a new brush with Duplicate Asset (see `creative-arts.animation.blender.brush-assets`).

## Gotchas

- Projected falloff treats points that overlap on screen as near each other, however far apart they are in the world.
- Remember the brush is an asset in 5.2: unsaved settings changes do not survive closing Blender.

## Verify

Test strokes on a plane: spacing gaps are absent, the falloff edge matches the chosen preset or curve, and stabilizer lag appears only when enabled.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release branch). Confirmed against sculpt_paint/brush/brush_settings, falloff and stroke: F, Shift-F, Ctrl-F, bracket keys, Size Unit (renamed from Radius Unit), the full falloff preset list including Smoother and Sharper, Falloff Shape, stroke method list and options, Alt-E, Shift-S, Stabilize Stroke Radius and Factor, temporary brush asset changes. Removed unconfirmed claims such as a default stroke method, a recommended 10 percent spacing and per-preset use cases.
Method: documentation only; no commands were run.
