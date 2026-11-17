---
id: creative-arts.animation.blender.holding-edges
name: holding-edges
category: creative-arts
field: animation
product: blender
tags: [blender, holding-edges, support-loops, subdivision-surface, hard-surface, edge-crease]
level: practitioner
status: docs-checked
description: "Control subdivision sharpness with holding edges: support loop placement and spacing, loop cuts and bevels, edge crease alternatives and avoiding pinching on hard-surface models."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/subdivision_surface.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/edge/loopcut_slide.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/edge/edge_data.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/normals/smooth_by_angle.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# holding-edges

Goal: crisp but softened edges on a subdivided hard-surface model, without shading ripples.

## The rule

Subdivision pulls each edge toward the average of its neighbours. A **support (holding) loop** placed close to an edge limits that pull: the closer the loop, the tighter the resulting corner radius.

## Adding them

- **Loop Cut and Slide** (`Ctrl R`, scroll for count, click, then slide; type a value or use *Even* `E`) for edge loops parallel to a border.
- **Bevel** (`Ctrl B`, *Bevel Edges*) with two *Segments* and a small width on the hard edge: creates support loops in one go, evenly spaced.
- **Inset** (`I`) on flat caps to create the loop around a face's border.
- Spacing sets the corner radius: tighter loops give a sharper edge, wider loops a softer one.

## Alternatives

- **Edge crease** (`Shift E`; the Subdivision Surface modifier respects it when *Use Creases* is on): sharpens without extra geometry, but the sharpness is crease data rather than geometry, so confirm your exporter keeps it.
- **Bevel modifier before Subdivision** (Limit Method Angle, a few Segments): procedural support loops; keep geometry clean underneath.

## Keeping shading clean

- Support loops must run all the way around (complete loops) or terminate into triangles/poles on flat areas, never on curved surfaces.
- Uneven spacing produces visible bulges; use *Even* slide or the bevel approach.
- Poles (3 or 5 edges) belong on flat areas; on curves they cause pinching.

## Gotchas

- Too many loops make later edits painful; add support last, after the base shape is final.
- The Subdivision Surface *Advanced* options *Use Limit Surface* and *Quality* affect vertex positions and how accurately creases work.
- With *Shade Auto Smooth* (the Smooth by Angle modifier), edges steeper than its *Angle* are shaded sharp, so very tight loops can be split; raise the angle or use plain smooth shading.

## Verify

Matcap (Studio → Metal or Reflection) view with Subdivision on: reflections flow smoothly across faces and tighten consistently at every edge; no ripples near poles.

## Checked

2026-10-27, Blender manual 5.2 (blender-v5.2-release RST). Confirmed: Loop Cut and Slide on Ctrl R with Even on E; Bevel Edges on Ctrl B with Segments and Profile Shape; Inset on I; Edge Crease on Shift E; Subdivision Surface Use Creases, Use Limit Surface and Quality; Smooth by Angle Angle setting. Removed: the percentage spacing figure, the 0-1 crease range, the 30 degree bevel angle and the claim that creases may not transfer to engines.

Method: documentation only; no commands were run.
