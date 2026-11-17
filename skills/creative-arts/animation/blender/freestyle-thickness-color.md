---
id: creative-arts.animation.blender.freestyle-thickness-color
name: freestyle-thickness-color
category: creative-arts
field: animation
product: blender
tags: [blender, freestyle-thickness, freestyle-color, freestyle-alpha, freestyle, line-style, npr]
level: practitioner
status: docs-checked
description: "Style Freestyle strokes: base colour, alpha and thickness, thickness position, and modifiers along stroke, distance from camera, material, curvature, noise and calligraphy."
sources:
  - https://docs.blender.org/manual/en/latest/render/freestyle/view_layer/line_style/index.html
  - https://docs.blender.org/manual/en/latest/render/freestyle/view_layer/line_style/modifiers/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# freestyle-thickness-color

Goal: lines that taper, fade with depth and pick up material colours, like inked artwork.

## Base properties (Freestyle Line Style)

- *Base Color*, alpha and *Base Thickness*. Whether thickness is absolute pixels or scaled to render height depends on Render Properties → Freestyle → *Line Thickness Mode* (Absolute or Relative).
- *Thickness Position*: Center, Inside, Outside, or Relative (a *Thickness Ratio* from 0.0 inside to 1.0 outside). It applies only to *Silhouette* and *Border* strokes; other edge types always use Center.

## Modifiers (Color, Alpha, Thickness tabs)

Every modifier has *Mix* (blend method with the base property) and *Influence*; Color modifiers also have a colour ramp.

| Modifier | What it does |
|---|---|
| Along Stroke | maps a range along each stroke's length (a gradient, taper) |
| Distance from Camera | maps distance to the active camera; *Range Min/Max* are in scene units, not pixels |
| Distance from Object | same, to a *Target* object (or the camera) |
| Material | takes the value from the material under the stroke; use *Split by Material* in the Strokes tab to avoid blending across materials |
| Crease Angle | maps crease angle (*Angle Min/Max*); non-crease segments are untouched |
| Curvature 3D | maps radial curvature (*Curvature Min/Max*); needs *Face Smoothness* on and Smooth Shading on the object |
| Noise | pseudo-random variation (*Amplitude*, *Period*, *Seed*); thickness also has *Asymmetric* |
| Tangent | based on the stroke's travel direction at its vertices |
| Calligraphy (thickness only) | broad-nib look from *Orientation*: strokes aligned with the angle are thickest, perpendicular ones thinnest |

*Fill Range by Selection* on the distance modifiers sets the range from the selected mesh vertices.

## Material line colour

Properties → Material → *Freestyle Line* panel: *Line Color* per material and *Priority* (ordering of competing line colours at material boundaries).

## Verify

Render a test frame: line ends taper, distant lines change as mapped, material line colours appear where set.

## Checked

2026-10-27 against the Blender 5.2 manual (Line Style Thickness, Color and modifier pages, Material Properties). Confirmed Thickness Position behaviour, modifier names and parameters and the Freestyle Line material panel. Removed unconfirmed claims about "100% resolution" pixels, the Material modifier using line colour, overlap darkening and zero-range behaviour.
Method: documentation only; no commands were run.
