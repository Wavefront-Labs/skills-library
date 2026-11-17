---
id: creative-arts.animation.blender.lock-relative-weights
name: lock-relative-weights
category: creative-arts
field: animation
product: blender
tags: [blender, weight-paint, lock-relative, locked-groups, multi-paint, auto-normalize]
level: practitioner
status: docs-checked
description: "Paint weights between bones in Blender with locked vertex groups, Lock-Relative display, Multi-Paint for several bones, and Auto Normalize interplay."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/weight_paint/tool_settings/options.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/properties/vertex_groups/vertex_groups.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/properties/vertex_groups/vertex_weights.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# lock-relative-weights

Goal: rebalance weights between specific bones while protecting the rest.

## Locking groups
Object Data > Vertex Groups: lock icon per group; a locked group cannot be edited, only renamed or deleted. Vertex Group Specials menu > **Lock All / Unlock All / Lock Invert All**.

## Lock-Relative (Options panel)
Displays bone-deforming groups as if all locked deform groups were deleted and the remaining ones re-normalized (so if locked groups take 0.4 of a vertex, the remaining 0.6 reads as 1.0). It is meant for balancing weights within a group of bones, say forearm and hand, while all other bones are locked, and can also show non-normalized weights as if they were normalized without changing the values.

## Multi-Paint
Options > **Multi-Paint**: select several pose bones (it only works from the Armature tab selection); once two or more groups are selected, the display shows the sum of their weights (the average if Auto Normalize is off) and painting changes the groups together while keeping their ratio. It cannot paint vertices with no weight in those groups and cannot reduce a weight to zero. Use it where more than three bones affect an area.

## Typical workflow for a joint
1. Lock everything except the two bones at the joint (Lock All, then unlock both).
2. Auto Normalize on, Lock-Relative on.
3. Paint/blur the transition: weight moves only between the two unlocked groups.

## Gotchas
- With all deform groups locked except one, Auto Normalize has nothing to redistribute to, so painting may appear to do nothing (practice).
- A locked group cannot be edited, so forgotten locks make later painting "not work"; use Unlock All.
- Lock-Relative changes the displayed weights (the manual: without changing the values); with Auto Normalize off, the manual notes Blender still normalizes over all deform bones for deformation.

## Verify
After painting, sums are unchanged for vertices outside the two bones' area (spot-check in the Sidebar's Vertex Weights panel).

## Checked

2026-10-27. Documentation release: Blender manual 5.2 (branch blender-v5.2-release). Confirmed: Auto Normalize, Lock-Relative and Multi-Paint behaviour, including the Multi-Paint limits (sculpt_paint/weight_paint/tool_settings/options.rst); per-group Lock and the Vertex Group Specials entries Lock All, Unlock All and Lock Invert All (modeling/meshes/properties/vertex_groups/vertex_groups.rst); the Vertex Weights panel in the 3D Viewport Sidebar (vertex_weights.rst). Wrong in the old text: there are no Lock Selected/Unselected entries in the specials menu, the Item tab and Edit mode wording was imprecise, and the claims that locked groups are excluded from Normalize All and that Ctrl-click selects bones were not in the manual and were removed.

Method: documentation only; no commands were run.
