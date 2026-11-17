---
id: creative-arts.animation.blender.weight-limit-clean
name: weight-limit-clean
category: creative-arts
field: animation
product: blender
tags: [blender, weight-paint, weight-limit-total, limit-total, clean-weights, game-export]
level: practitioner
status: verified
description: "Prepare Blender skin weights for export: Limit Total, Clean with Keep Single, Subset options, and the order to run them with Normalize All."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/weight_paint/editing.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# weight-limit-clean

Goal: tidy weights so a target engine's influence cap does not change the look of the deformation.

## Limit Total
Weights > **Limit Total** (also in Edit Mode): reduces the number of weight groups per vertex to **Limit**, removing the lowest weights first. **Subset** restricts it to Active Group, Selected Pose Bones, Deform Pose Bones or All Groups (on a mesh with no armature the operator offered only All Groups). The manual notes it only works reasonably when more than one group is in the subset. Choose Limit from your engine's documented per-vertex influence cap. The operator is `bpy.ops.object.vertex_group_limit_total(group_select_mode=, limit=)`; `limit` defaults to 4 and accepts 1 to 32 (tested: a vertex with weights 0.6, 0.3 and 0.05 kept the 0.6 and 0.3 groups at limit 2).

## Clean
Weights > **Clean**: **Limit** is the minimum weight kept; weights below it are removed from the group. **Keep Single** stops Clean from leaving a vertex in no group at all (each vertex keeps at least one weight even if below the limit). **Subset** as above. Use it to clear very low or zero weights, which otherwise take up influence slots. The operator is `bpy.ops.object.vertex_group_clean(group_select_mode=, limit=, keep_single=)`: `limit` defaults to 0.0 (range 0 to 1) and `keep_single` to False. Tested: with limit 0.5 a vertex whose weights were 0.01 and 0.02 ended in no group, and with `keep_single=True` it kept one weight, the one from the first group (0.01), not the larger one.

## Order
1. Clean (small Limit, Keep Single on, Subset Deform Pose Bones).
2. Limit Total (engine cap).
3. Normalize All (see weight-normalize).
4. Optionally Quantize if the target stores weights at low precision (Steps = number of weight levels between 0 and 1).

## Gotchas
- Choose a Subset that is only the deform groups; with All Groups, utility groups (masks, cloth pins) are cleaned and limited too.
- Limit Total changes the sum of weights, so run Normalize All afterwards.

## Verify
Edit Mode > Spreadsheet (Vertex domain) or a script over `mesh.vertices[i].groups`: no vertex has more groups than the cap, and deform weights sum to 1.

## Checked
Date: 2026-10-27. Documentation: Blender manual, Weight Paint Editing page, branch blender-v5.2-release. Confirmed: Weights menu entries Limit Total and Clean, the Limit, Keep Single and Subset options and their meanings, lowest-first removal, the single-group caveat, and Quantize steps. Removed unconfirmed claims: 4 or 8 as typical caps, engine behaviour on excess influences, FBX and engine import options, tie asymmetry after Limit Total, and a claim about Clean on all groups.
Run check, 2026-11-01, Blender 4.5.14 LTS headless: both operators ran in Edit Mode on a UV sphere with three groups; Limit Total, Clean and Keep Single behaved as above; property ranges came from the operator definitions. Unrun: the Subset values that need an armature, the single-group caveat, Quantize in this context, UI menu paths.
Method: documentation checked against the manual and API pages; the code and operators were run headless in Blender 4.5.14.
