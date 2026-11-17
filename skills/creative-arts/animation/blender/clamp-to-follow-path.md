---
id: creative-arts.animation.blender.clamp-to-follow-path
name: clamp-to-follow-path
category: creative-arts
field: animation
product: blender
tags: [blender, constraints, clamp-to, clamp-to-constraint, follow-path, follow-path-constraint, evaluation-time, path-animation]
level: practitioner
status: docs-checked
description: "Move objects along curves in Blender: Follow Path (offset, Follow Curve, Animate Path, Evaluation Time) and Clamp To (position mapped along a curve by an axis, cyclic)."
sources:
  - https://docs.blender.org/manual/en/5.2/animation/constraints/relationship/follow_path.html
  - https://docs.blender.org/manual/en/5.2/animation/constraints/tracking/clamp_to.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# clamp-to-follow-path

## Follow Path

1. Quick setup: select the object, add the curve to the selection, Ctrl-P, Path Constraint. Or add the constraint by hand and set Target to the curve.
2. The owner's world position and rotation act as offsets from the curve point, so clear them first (Alt-G, Alt-R) to sit exactly on the curve. The curve's scale multiplies the position offset.
3. **Animate Path** animates the curve's Evaluation Time so it equals the current scene frame; you can also animate Evaluation Time by hand. **Offset** (Fixed Position off) is the number of frames subtracted from the Evaluation Time.
4. **Follow Curve** with **Forward Axis** and **Up Axis** rotates the owner along the curve tangent (vehicles, cameras on rails). The two axes must differ or the constraint stops working and its icon turns red.
5. **Fixed Position** + **Offset Factor** (0 to 1) ignores Evaluation Time; animate the factor to move along the curve.
6. **Curve Radius** scales the owner by the radii of the curve's control points.
- Follow Path can be combined with a tracking constraint, for example to keep a moving camera pointed at an object.

## Clamp To

- Snaps the owner to a curve by remapping its coordinate along the **Main Axis** (chosen automatically from the longest side of the curve's bounding box if none is set) to 0-1 along the curve. **Cyclic** makes the owner jump to the opposite side instead of stopping at the ends, mainly useful with closed curves.
- The owner's coordinate is read in world space but the bounding box in the curve's local space, so keep the curve object at default rotation for intuitive results. Bezier handles and point radii count towards the bounding box.
- If the owner moves the wrong way along the curve, use Switch Direction on the curve.
- Keys live in the owner's own location, no Evaluation Time needed. It positions only; Follow Path can also orient.

## Recipes

- **Camera dolly track**: Bezier path, camera Follow Path with Fixed Position, key Offset Factor with ease; Track To an Empty for aim (see `camera-cinematography`).
- **Bead on a wire**: Clamp To, Main Axis X, Cyclic on a closed curve.

## Gotchas

- Owner not at world origin or with rotation: it follows the path with an offset (most "it's off the path" cases).
- Follow Curve with Forward Axis equal to Up Axis disables the constraint (red icon).

## Verify

Object sits exactly on the curve throughout; speed changes match the Evaluation Time/Offset curve.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release). Confirmed on the Follow Path and Clamp To constraint pages: Animate Path, Offset and Offset Factor, Fixed Position, Follow Curve, Forward/Up Axis rule, Curve Radius, Main Axis auto-selection, Cyclic and bounding box behaviour, Ctrl-P Path Constraint, Alt-G/Alt-R offsets. Removed unconfirmed Path Animation panel (Frames, extrapolation) and curve twist method advice.

Method: documentation only; no commands were run.
