---
id: creative-arts.animation.principles.arc-tracking
name: arc-tracking
category: creative-arts
field: animation
product: principles
tags: [animation, motion-arcs, arc-tracking, onion-skin, motion-trails, motion-paths, arcs, polish, blender, maya, 2d]
level: practitioner
status: draft
description: "Track and clean motion arcs with onion skins, motion trails and on-screen arc marks: which points to track, how to spot breaks, and fixing them."
sources:
  - https://books.google.com/books?vid=ISBN9780865478978
  - https://docs.blender.org/manual/en/latest/animation/motion_paths.html
  - https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Arc tracking

Goal: verify that organic motion travels on smooth arcs and fix the frames that break them.
Almost every natural action follows an arc; broken arcs read as mechanical or jittery.

## What to track
- Nose tip or between the eyes (head arcs).
- Wrist or fingertip (hand arcs).
- Centre of mass / pelvis (body path in walks and jumps).
- Tips of appendages (tail, ear, hair end).
Track one point at a time; a messy arc on one point is usually the real problem.

## Tools
- **2D**: onion skin 3-5 frames each side, or mark the point on each drawing with a dot on a
  separate layer and connect the dots.
- **Blender**: Pose Mode, select bone > Properties > Bone > Motion Paths > Calculate
  (or Object/Pose > Motion Paths), "Around Frame" range; shows frame dots so spacing is visible
  too.
- **Maya**: Animation > Create Editable Motion Trail; or a grease-pencil/arc-tracker script
  that draws on the viewport.
- **Any software**: screen-capture or a transparent overlay drawn on the monitor
  (a whiteboard marker on a screen protector is a classic studio trick).

## Spotting breaks
- A dot sitting off the curve: a pop.
- A sharp corner in the path where no direction change was intended.
- Uneven dot gaps when the move should ease (spacing problem, not arc problem).
- Zig-zags from two controls (e.g. FK shoulder + IK wrist) fighting.

## Fixing
1. Find the offending frame; adjust the pose on that frame only (or the nearest key).
2. In CG, add a breakdown key to pull the path back onto the curve rather than editing
   multiple tangents blindly.
3. Recalculate the trail and check spacing again.

## Verify
- [ ] Head and hand paths are smooth curves through every acting move.
- [ ] Corners exist only at intended direction changes/impacts.
- [ ] Spacing along the arc matches the intended ease.

Related: `creative-arts.animation.principles.arc-pops-and-ik-fk-breaks`,
`creative-arts.animation.principles.head-and-hand-arcs`.
