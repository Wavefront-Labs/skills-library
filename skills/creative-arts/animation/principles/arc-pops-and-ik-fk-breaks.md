---
id: creative-arts.animation.principles.arc-pops-and-ik-fk-breaks
name: arc-pops-and-ik-fk-breaks
category: creative-arts
field: animation
product: principles
tags: [animation, motion-arcs, arc-pops, ik-fk, ik-fk-switch, gimbal-lock, euler-filter, polish, cg, maya, blender]
level: advanced
status: draft
description: "Diagnose and fix CG arc pops: IK straight-line interpolation, IK/FK switch frames, gimbal flips and space switches that break smooth arcs."
sources:
  - https://docs.blender.org/manual/en/latest/animation/armatures/posing/bone_constraints/inverse_kinematics/introduction.html
  - https://docs.blender.org/manual/en/latest/editors/graph_editor/introduction.html
  - https://books.google.com/books?vid=ISBN9780865478978
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Arc pops and IK/FK breaks

Goal: find the technical causes of broken arcs in CG and fix them at the source.

## Common causes
1. **IK translation between keys**: an IK hand interpolates in a straight line between two
   keyed positions, so a swinging arm has a flat arc. Fix: add breakdown keys on the arc, or
   use FK for swinging/arcing arms (FK rotations naturally produce arcs).
2. **IK/FK switch frame**: the limb pops on the switch frame because IK and FK poses do not
   match. Fix: match/snap IK to FK (or FK to IK) on the switch frame with the rig's match tool,
   key both, and step the blend attribute (constant interpolation) or blend over 2-3 frames.
3. **Space switching** (hand parented to world vs chest): the hand jumps when the parent space
   changes. Fix: key the switch with the rig's "match space" tool so world position is kept.
4. **Gimbal flips / Euler discontinuity**: rotation curves jump by about 360 or 180 degrees,
   the limb spins through an unexpected path. Fix: Blender Graph Editor > Channel >
   Discontinuity (Euler) Filter; Maya Graph Editor > Curves > Euler Filter. Or change rotation
   order, or use quaternions for that control.
5. **Pole vector flips**: the knee/elbow snaps when the pole crosses the limb plane; key the pole.
6. **Counter-animation**: a parent and child both moving in opposite directions cancelling arcs.

## Method
1. Turn on motion trails for the popping point; find the exact frame.
2. Check the graph editor for that control's curves at that frame: jumps, switch attributes,
   space attributes.
3. Fix at the cause (match switch, filter Euler, add breakdown), not by nudging the pose until
   it looks OK on one frame.

## Verify
- [ ] Motion trail smooth through switch frames.
- [ ] No rotation curve jumps of about 180/360 degrees.
- [ ] Blend/space attributes keyed with matched poses.

Related: `creative-arts.animation.principles.arc-tracking`.
