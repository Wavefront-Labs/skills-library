---
id: creative-arts.animation.blender.weight-paint-bone-select
name: weight-paint-bone-select
category: creative-arts
field: animation
product: blender
tags: [blender, weight-paint, weight-paint-bone-select, weight-paint-face-mask, armature, pose-while-painting]
level: practitioner
status: docs-checked
description: "Weight paint with the armature in Blender: enter with the rig selected, Ctrl+click bones to switch groups, pose while painting, and face/vertex masking."
sources:
  - https://docs.blender.org/manual/en/5.2/sculpt_paint/weight_paint/usage.html
  - https://docs.blender.org/manual/en/5.2/sculpt_paint/weight_paint/introduction.html
  - https://docs.blender.org/manual/en/5.2/sculpt_paint/weight_paint/tool_settings/options.html
  - https://docs.blender.org/manual/en/5.2/sculpt_paint/weight_paint/editing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# weight-paint-bone-select

Goal: see deformation live and switch target bones without leaving the brush.

## Entering correctly (manual procedure)

1. Select the armature and bring it into Pose Mode (Ctrl-Tab).
2. Make sure Edit > Lock Object Modes is unchecked in the top bar.
3. Select the mesh and bring it into Weight Paint Mode.
4. Make sure **Bone Selection** is checked in the 3D Viewport header.
5. Select a bone with **Alt-LMB** (or Shift-Ctrl-LMB): its vertex group becomes active and its weights are shown. Only one bone can be selected at a time in this mode.
6. Paint with LMB. If a bone has no vertex group yet, Blender creates one automatically when you start painting.
- Bones embedded in the mesh may be invisible or unselectable; enable **In Front** for the armature.
- With a symmetrical mesh and armature, Mirror Vertex Groups can create the groups and weights for the other side.

## Masking and weight options

- The Weights menu tools (Assign Automatic from Bone, Normalize All, Smooth and so on) respect Vertex Selection Masking and Face Selection Masking, operating only on selected vertices or faces.
- **Restrict** limits painting to vertices belonging to the selected vertex group. **Auto Normalize** keeps deforming groups adding up to one while painting; **Lock-Relative** shows groups as if locked groups were deleted and the rest re-normalized; **Multi-Paint** paints on all selected vertex groups together, preserving their ratio (select several pose bones; it cannot paint on vertices with no weight in those groups).
- Unreferenced vertices can be shown in black through the Viewport Overlays weight paint options.

## Gotchas

- Plain Ctrl-click is not the documented bone selection; use Alt-LMB or Shift-Ctrl-LMB, and keep Lock Object Modes off so the armature stays in Pose Mode.
- If bones cannot be picked, check that Bone Selection is enabled in the header and that the armature has In Front on.

## Verify

Select a bone: its vertex group becomes active and the weight display shows that group; painting changes only that group (or the selected groups with Multi-Paint).

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release). Confirmed on the Weight Paint Using Vertex Groups, Introduction, Options and Editing pages: pose-mode and Lock Object Modes procedure, Bone Selection toggle, Alt-LMB or Shift-Ctrl-LMB selection (not plain Ctrl-click), automatic group creation, In Front tip, Restrict, Auto Normalize, Lock-Relative, Multi-Paint, selection masking in tools. Removed the unconfirmed overlay item names, hide shortcut and pose-position remarks.

Method: documentation only; no commands were run.
