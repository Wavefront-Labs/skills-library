---
id: creative-arts.animation.blender.breakdown-slide
name: breakdown-slide
category: creative-arts
field: animation
product: blender
tags: [blender, animation, breakdown-slide, relax-pose, push-pose, breakdowner, push-pull-keys, pose-breakdowner, blend-to-neighbour, pose-mode]
level: practitioner
status: docs-checked
description: "Create favoured breakdowns and tweak poses in Blender: Pose Breakdowner (Shift E), Push/Relax Pose, Blend to Neighbour, and the Graph Editor slider tools (Ease, Blend to Default, Push/Pull)."
sources:
  - https://docs.blender.org/manual/en/latest/animation/in_betweens.html
  - https://docs.blender.org/manual/en/latest/editors/graph_editor/fcurves/editing.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# breakdown-slide

Goal: breakdowns that favour one key (the classic 1/3 or 2/3 inbetween) without re-posing by hand.

## Pose Mode in-betweens (Pose > Animation > In-Betweens)

- **Pose Breakdowner (Shift E)**: interactively slide the pose between the previous and next keyframe by moving the mouse. While it is active, restrict it with G/R/S (move, rotate, scale), B (bendy bones), C (custom properties) and X/Y/Z (axes).
- **Push Pose from Breakdown (Ctrl E)**: pushes the pose away from the linear interpolation between the surrounding keys.
- **Relax Pose to Breakdown (Alt E)**: the opposite; at full influence the pose equals the linear interpolation between the surrounding keys.
- **Blend to Neighbor (Shift Alt E)**: blends the current pose toward the neighbouring keyframes; needs a keyframe before and after the current frame.
- **Blend Pose with Rest Pose**: interpolates the pose to the rest position (a negative factor moves away from it); needs only one keyframe.
Insert a key afterwards (or have auto keying on).

## Graph Editor key sliders (Key > Blend, Alt D)

With keys selected, Key > Blend offers **Breakdown**, **Blend to Neighbor**, **Blend to Default Value**, **Ease**, **Blend Offset**, **Blend to Ease**, **Match Slope**, **Push Pull**, **Shear Keys**, **Scale Average**, **Scale from Neighbor** and **Time Offset**. Cleanup smoothing is under Key > Smooth: **Smooth (Gaussian)**, **Butterworth Smooth** and **Smooth (Legacy)**. Each is interactive: choose the item, move the mouse to set the amount, then confirm.

## Workflow

1. Block key poses on twos-stepped.
2. Add breakdowns: at the frame between, Shift E, favouring the destination for snappy motion (about 0.7, a practice value) or the start for slow-in.
3. Graph Editor: Ease and Blend to Neighbor to refine spacing on individual curves.

## Gotchas

- The in-between tools build the pose from the keys surrounding the current frame, so keys must exist before and after it; the 0.7 favouring value above is practice, not from the manual.

## Verify

Onion skin/motion path (see `markers-motion-paths`): breakdown sits on the arc at the intended favouring.

## Checked

2026-10-27. Documentation release: Blender manual 5.2 (branch blender-v5.2-release) plus the Pose menu definitions in space_view3d.py (VIEW3D_MT_pose_slide, labelled In-Betweens, under Pose > Animation). Confirmed in animation/in_betweens.rst: Pose Breakdowner Shift E with G/R/S, B, C, X/Y/Z constraints, Push Pose Ctrl E, Relax Pose Alt E, Blend to Neighbor Shift Alt E, Blend Pose with Rest Pose. Confirmed in editors/graph_editor/fcurves/editing.rst: the Key > Blend items (Alt D) and the Key > Smooth items. Wrong in the old text: there is no Push/Relax Pose from Rest Pose item (it is Blend Pose with Rest Pose), and the menu path was Pose > Animation > In-Betweens. Removed the Ctrl-for-precision claim and the selected-bones-only gotcha, which no source confirms.

Method: documentation only; no commands were run.
