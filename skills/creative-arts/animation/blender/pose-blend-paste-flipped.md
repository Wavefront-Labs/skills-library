---
id: creative-arts.animation.blender.pose-blend-paste-flipped
name: pose-blend-paste-flipped
category: creative-arts
field: animation
product: blender
tags: [blender, pose-library, pose-blend-flipped, blend-pose, apply-pose-flipped, copy-paste-pose, paste-flipped, copy-pose]
level: practitioner
status: docs-checked
description: "Apply and blend poses in Blender: pose asset apply/flipped/blend, shelf drag, and Copy/Paste/Paste Flipped Pose (Ctrl-C, Ctrl-V, Shift-Ctrl-V) between frames and sides."
sources:
  - https://docs.blender.org/manual/en/5.2/animation/armatures/posing/editing/pose_library.html
  - https://docs.blender.org/manual/en/5.2/animation/armatures/posing/editing/copy_paste.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# pose-blend-paste-flipped

## Pose assets

- Asset shelf (3D Viewport, Pose Mode): **click** a pose to apply it; the cursor keys also select and apply. **Drag the thumbnail left to right** to blend it into the current pose (release to confirm).
- Asset Browser, right-click a pose: **Apply Pose** (only to selected bones if any are selected; double-click also applies), **Apply Pose Flipped** (mirrors left and right), **Blend Pose**, **Select/Deselect Pose Bones** (shows which bones the pose uses).
- **Blend Pose**: click, move the mouse left/right; dragging left subtracts the pose; Tab toggles original and blended; LMB/Return confirms, RMB/Esc cancels; **E** extrapolates beyond 100 percent. Hold **Ctrl** while blending to blend the flipped pose.
- With several armatures in Pose Mode, a matching slot of the pose asset is chosen per armature.

## Copy / Paste pose (Pose menu, Pose Mode)

- **Ctrl-C** Copy Pose, **Ctrl-V** Paste Pose, **Shift-Ctrl-V** Paste Pose Flipped (X-axis mirrored).
- One session-level pose buffer, usable across armatures, scenes and files; it is not saved with the file.
- Only the selected bones are copied; on paste, bone selection does not matter and the pose is applied per bone name (bones with no matching name are ignored).
- What is copied is each bone's position, rotation or scale in its own space, so the result can differ with different rest positions or parent poses.

## Recipes

- Hold a pose across frames: copy at one frame, paste at a later one, then insert keys (I).
- Opposite step of a walk: copy a contact pose, move half a cycle on, Paste Pose Flipped, then key.
- Hand shapes: blend between `relaxed` and `fist` assets for a loose grip.

## Gotchas

- Flipped pasting relies on mirrored bone names and a symmetric rig; asymmetric rest rolls give wrong rotations.
- Copied poses are per name: a rig with different bone names receives nothing.

## Verify

Paste Pose Flipped of a raised left arm raises the right arm identically (check from the front); blending moves smoothly between 0 and 100 percent.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release source), Pose Library and Copy/Paste Pose pages: shelf click/drag, Apply/Apply Flipped/Blend/Select bones, Blend Pose keys (Tab, E, Ctrl), Copy/Paste shortcuts and buffer behaviour. Removed as unconfirmed: auto-keying interaction with applying, redo-panel paste options, root X flip remark, walk frame numbers. Corrected: paste ignores selection (the skill's Selected Only option is not documented).
Method: documentation only; no commands were run.
