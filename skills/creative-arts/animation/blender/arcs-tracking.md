---
id: creative-arts.animation.blender.arcs-tracking
name: arcs-tracking
category: creative-arts
field: animation
product: blender
tags: [blender, character-animation, arcs-tracking, arc-tracking, motion-paths, polish, spacing]
level: practitioner
status: docs-checked
description: "Track and fix arcs in Blender polish passes: helper bones/empties at nose and fingertips, motion paths, camera-space tracking, and fixing kinks via breakdowns and Graph Editor rotation curves."
sources:
  - https://docs.blender.org/manual/en/latest/animation/motion_paths.html
  - https://docs.blender.org/manual/en/latest/animation/in_betweens.html
  - https://docs.blender.org/manual/en/latest/editors/graph_editor/introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# arcs-tracking

Goal: natural motion follows arcs; kinks, zig-zags and linear paths read as mechanical.

## What to track

Nose/top of head, wrists/fingertips, COG/hips, toe in swing, tail tip. The tip of an FK chain shows the combined result of all parent rotations.

## Setup

- Add a small bone (non-deforming) at the fingertip/nose parented to the hand/head bone, select it in Pose Mode and calculate its motion path with Bake Location set to Tails (see `motion-path-settings`). Use a range that covers the shot, or the Around Frame paths type for long shots.
- Turn on Keyframes display to see which points are keys.
- Camera space: arcs read on screen, not in world space. Enable **Bake to Active Camera** when calculating the path so it is computed in screen space for the active scene camera; the result is only valid for that one camera, and switching cameras with markers is not supported.

## Fixing

- **Kink at a key**: the key's spacing or pose is off the arc — adjust the pose (rotate parent bones, not IK target translation alone) so the point sits on the arc.
- **Zig-zag between keys**: rotation curves in the Graph Editor on parent bones have opposing eases — align handles or add a breakdown (Pose Breakdowner, Shift E) on the arc.
- **Linear path in IK**: IK controls interpolate in straight lines — add breakdowns that push the IK control onto the arc, or animate that section in FK.
- Paths update automatically when you edit poses and keyframes; use Update Paths if a path looks stale.

## Gotchas

- Fixing arcs on the fingertip by moving only the hand can break the elbow arc — work top-down (shoulder → elbow → wrist).
- Euler interpolation of large rotations can create looping arcs (practice, not from the manual); use quaternions for those bones or add keys.

## Verify

Paths show smooth curves with even spacing transitions; no hooks or sharp corners except at intended direction changes (hits). The what-to-track list and fixing order are animation practice rather than Blender documentation.

## Checked

2026-10-27. Documentation release: Blender manual 5.2 (branch blender-v5.2-release). Confirmed: Motion Paths Calculate with Bake Location Heads/Tails, Paths Type Around Frame/In Range, Keyframes display, Update Paths, and the Bake to Active Camera option (screen space, single camera, no marker switching) in animation/motion_paths.rst; Pose Breakdowner is Shift E in animation/in_betweens.rst. Removed the parent-an-empty-to-the-camera workaround, which the manual does not describe.

Method: documentation only; no commands were run.
