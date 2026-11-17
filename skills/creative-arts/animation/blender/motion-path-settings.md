---
id: creative-arts.animation.blender.motion-path-settings
name: motion-path-settings
category: creative-arts
field: animation
product: blender
tags: [blender, motion-paths, motion-path-range, calculate-motion-path, update-motion-paths, motion-path-display, motion-path-frame-numbers, arcs]
level: practitioner
status: docs-checked
description: "Configure Blender motion paths for arc checks: range (scene, selected keys, around frame), heads vs tails, updating after edits, and display of frame numbers and keyframes."
sources:
  - https://docs.blender.org/manual/en/latest/animation/motion_paths.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# motion-path-settings

Goal: visible arcs for the parts you're polishing — nose, wrists, hips — that stay up to date as you edit. Broader use with markers is in `markers-motion-paths`.

## Calculate (Object or Armature/Bone properties > Motion Paths)

- **Paths Type**: *In Range* (fixed Start/End) or *Around Frame* (Before/After window around the current frame; the manual notes playback only affects paths for this type).
- **Calculation Range** (In Range only): *All Keys* (first to last key of the active object/bone), *Selected Keys*, *Scene Frame Range* (or the preview range if active), *Manual Range*. Updating a path resets Start/End from this setting unless it is Manual Range.
- **Step**: show one point every n frames; 1 for polish.
- **Bake Location** (bones, Pose Mode, in the Calculate pop-up): *Heads* or *Tails* — the bone root or the bone tip. Which one lands on the nose or crown depends on how the rig's bone is built.
- **Bake to Active Camera**: calculates the path in screen space for the active scene camera only.
- **Calculate** (Pose > Motion Paths > Calculate; select the bones first), **Update Paths** after edits, **Update All Paths**, and **Clear Paths** (the x button; Shift-click clears only the selected).
- The manual says paths update automatically when you edit poses and keyframes; use Update Paths if a path still looks stale, for example after changing constraint targets, parents or drivers (a practice note).

## Display

- **Frame Numbers** (show frame number at each point), **Keyframes** (big yellow squares on keyed frames), **+ Non-Grouped Keyframes** (searches the whole action, slower), **Keyframe Numbers**, **Lines** (connecting line), **Thickness**, **Custom Color** (for time before and after the current frame).
- Spacing reading: dots close together = slow; spread = fast.

## Tips

- Add a small helper bone/empty at the nose or fingertip and calculate its path for exact arcs.
- Paths are drawn in world space unless **Bake to Active Camera** is on; for a moving camera use that option to read the arc as the camera sees it (valid for that camera only).

## Gotchas

- Long ranges on heavy rigs are likely to be slow to calculate (practice); use Around Frame.
- The Cache/Bone Cache From and To range cannot be changed without deleting the path and calculating again.

## Verify

Path shows keyed frames highlighted, smooth arc without kinks at breakdown frames.

## Checked

2026-10-27. Documentation release: Blender manual 5.2 (branch blender-v5.2-release), animation/motion_paths.rst, plus the Pose > Motion Paths menu in space_view3d.py. Confirmed: Paths Type Around Frame/In Range, Calculation Range options, Step, Bake Location Heads/Tails, Bake to Active Camera, Calculate, Update Paths, Update All Paths, Clear Paths (Shift for selected only), Cache From/To limitation, and the Display options Frame Numbers, Keyframes, Non-Grouped Keyframes, Keyframe Numbers, Lines, Thickness, Custom Color. Wrong in the old text: Calculation Range is a separate setting from Paths Type, paths do update automatically on pose and key edits, and the camera-space workaround is superseded by Bake to Active Camera.

Method: documentation only; no commands were run.
