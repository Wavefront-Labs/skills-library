---
id: creative-arts.animation.blender.fcurve-envelope-limits
name: fcurve-envelope-limits
category: creative-arts
field: animation
product: blender
tags: [blender, fcurve-modifiers, envelope-modifier, envelope-control-points, envelope-reference, limits-modifier, fcurve-limits, clamp-animation]
level: practitioner
status: docs-checked
description: "Reshape and clamp F-curves with Blender's Envelope modifier (reference, min/max, control points) and Limits modifier (min/max X and Y), e.g. damping mocap or stopping floor dips."
sources:
  - https://docs.blender.org/manual/en/5.2/editors/graph_editor/fcurves/modifiers.html
  - https://docs.blender.org/manual/en/5.2/editors/graph_editor/channels/editing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# fcurve-envelope-limits

Goal: change a curve's overall amplitude over time, or hard-clamp it, without touching keys (mocap and baked data especially).

## Envelope

- You define an envelope of two horizontal lines that roughly match the curve's lower and upper bounds; control points then push, squeeze and stretch the envelope, and the curve with it, at a given frame.
- **Reference**: the value the envelope is centred around.
- **Min / Max**: offsets from the reference to the initial lower and upper bound.
- **Add Control Point**: adds a point at the current frame; each point has **Frame** and its own **Min / Max** offsets (the adjusted bounds at that frame).
- Use: grow a sway's amplitude over a shot, damp mocap arm swing in the second half, fade a cycle.

## Limits

- **Minimum / Maximum X**: removes the original curve data left of the minimum and right of the maximum frame, replacing it with constant extrapolation.
- **Minimum / Maximum Y**: clamps values so they never go below the minimum or above the maximum (a foot's Z never below 0; an eyelid never past closed).
- A hard clamp creates flat plateaus with sharp corners.

## Workflow

1. Select the channel, Channel > Add F-Curve Modifier (Shift-Ctrl-M) > Envelope or Limits; edit in Sidebar > Modifiers.
2. Use **Restrict Frame Range** (Start/End, Blend In/Out) for local application and **Influence** to blend with the original curve.
3. When final, Channel > Bake Channels with **Bake Modifiers** on turns the modified curve into keys and deletes the modifiers.

## Gotchas

- Modifiers evaluate top to bottom; drag to reorder.
- Rotation curves are in radians, so Limits Y values for rotation are radians.
- For rig-level limits prefer Limit Rotation/Location constraints, which affect posing and not only playback.

## Verify

The modified curve stays within the limits in the Graph Editor; amplitude changes where the control points sit.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release source): Envelope fields (Reference, Min/Max as offsets, Add Control Point, Frame, Min/Max), Limits X/Y behaviour, shared Influence and Restrict Frame Range, modifier order, Shift-Ctrl-M, Bake Channels with Bake Modifiers. Removed as unconfirmed: the "inverts or exaggerates oddly" claim, the "small diamonds" appearance. Corrected: Envelope Min/Max are offsets from the reference, not absolute bounds.
Method: documentation only; no commands were run.
