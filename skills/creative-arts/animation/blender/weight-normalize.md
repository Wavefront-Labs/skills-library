---
id: creative-arts.animation.blender.weight-normalize
name: weight-normalize
category: creative-arts
field: animation
product: blender
tags: [blender, weight-paint, weight-normalize, normalize-all, auto-normalize, skinning]
level: practitioner
status: verified
description: "Normalize skin weights in Blender: Normalize vs Normalize All (Lock Active), Auto Normalize and Lock-Relative while painting, and locked groups."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/weight_paint/editing.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/weight_paint/tool_settings/options.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# weight-normalize

Goal: each vertex's deform weights sum to 1.0 so the result is predictable in other tools.

## Why
Blender always normalises weights relative to each other across deform bones, so strict normalisation is not needed for animation inside Blender and further normalizing should not affect it. Normalising matters when another application reads the raw weights and expects a sum of 1.

## Tools
- Weights > **Normalize** (`bpy.ops.object.vertex_group_normalize()`): acts on the active group only; all vertices keep their relative weights, scaled so the highest weight is 1.0 (tested: 0.4 and 0.2 became 1.0 and 0.5, other groups unchanged). It does not make per-vertex sums equal 1.
- Weights > **Normalize All**: per vertex, makes the weights across all vertex groups sum to 1. Locked groups keep their values. **Lock Active** keeps the active group's values while normalizing all the others. The operator is `vertex_group_normalize_all(group_select_mode=, lock_active=)` and `lock_active` defaults to True. Tested: 0.4, 0.1, 0.1 became 0.667, 0.167, 0.167; with Lock Active on the first group, 0.4, 0.3, 0.3; with the third group locked at 0.1, 0.72, 0.18, 0.1.
- Paint Options > **Auto Normalize**: while painting, all deforming groups are kept summing to 1. It works most intuitively on weights already normalized with another tool. With it off, weights can be anything from 0 to 1.
- Paint Options > **Lock-Relative**: displays bone-deforming groups as if locked deform groups were deleted and the rest renormalized; useful for balancing a few bones while the others are locked, and for viewing non-normalized weights as if normalized without changing them.
- **Multi-Paint** (Options): paint on several selected groups at once while keeping their ratio (select multiple pose bones in the Armature tab).

## Workflow
1. Lock the groups you are happy with.
2. Normalize All (Lock Active if one group should stay fixed).
3. Paint with Auto Normalize on.

## Gotchas
- Normalize All works across all vertex groups, so non-deform groups (masks, cloth pins) are included unless locked; lock them first.
- Normalize cannot create weights: a vertex in no deform group stays unweighted (tested).

## Verify
Edit Mode > Spreadsheet, or a script: the sum of each vertex's deform group weights is 1 within a small tolerance.

## Checked
Date: 2026-10-27. Documentation: Blender manual, Weight Paint Editing and Options pages, branch blender-v5.2-release. Confirmed: Normalize and Normalize All behaviour, Lock Active, locked groups untouched, Auto Normalize, Lock-Relative and Multi-Paint descriptions, Blender's internal normalisation. Removed unconfirmed claims: Subset option on Normalize All, Alembic and USD skinning behaviour, Preserve Volume interaction, the Auto Normalize armature-modifier requirement, the ungrouped-vertex selection path, and single-group behaviour of Subtract.
Run check, 2026-11-01, Blender 4.5.14 LTS headless: Normalize, Normalize All, Lock Active and locked groups (`VertexGroup.lock_weight`) behaved as above in Edit Mode; `scene.tool_settings` has `use_auto_normalize`, `use_lock_relative` and `use_multipaint`. Unrun: how Auto Normalize, Lock-Relative and Multi-Paint change brush strokes (UI), Blender's internal normalisation, the Armature tab selection.
Method: documentation checked against the manual and API pages; the code and operators were run headless in Blender 4.5.14.
