---
id: creative-arts.animation.blender.weight-mirror
name: weight-mirror
category: creative-arts
field: animation
product: blender
tags: [blender, weight-paint, weight-mirror, mirror-vertex-group, x-mirror, topology-mirror, skinning]
level: practitioner
status: verified
description: "Mirror skin weights left to right in Blender: the Mirror tool options, Mirror Vertex Groups painting, Topology Mirror, the mirror-to-opposite-bone recipe."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/weight_paint/editing.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/weight_paint/tool_settings/symmetry.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# weight-mirror

Goal: weight one side, get an identical opposite side.

## Naming
Groups need symmetrical names, such as suffixes `.R`/`.L` or `_R`/`_L` (same conventions as bones, see the manual's armature naming conventions), or words like right/left.

## Mirror tool
Weights > **Mirror** (Mirror Vertex Group; Edit Mode and Weight Paint Mode). It mirrors weights from one side of a perfectly symmetrical mesh to the other; vertices with no counterpart are unaffected. The weights are not transferred to the opposite bone's group by themselves. The rest pose must be perfectly symmetrical across X.
- **Mirror Weights**: each selected vertex receives the weights of its symmetrical counterpart. If both are selected they swap; if only one is selected, the unselected one overwrites it. Active group only, unless All Groups is on.
- **Flip Group Names**: selected vertices in the active group (or its symmetrical group) are re-assigned to the symmetrical group, keeping their weight. With All Groups it applies to all such groups.
- **All Groups**: operate on all vertex groups.
- **Topology Mirror**: approximate mirror for meshes that are not fully symmetric.
- Operator `bpy.ops.object.vertex_group_mirror(mirror_weights=True, flip_group_names=True, all_groups=False, use_topology=False)`; the defaults are shown, so switch Flip Group Names off when you only want Mirror Weights.

## Mirror to the opposite bone
1. Delete the target vertex group.
2. Duplicate the source group and rename the copy to the target group's name.
3. Select the target group and run Mirror with only Mirror Weights (plus Topology Mirror if the mesh is not symmetric).

## Paint symmetrically
Tool settings > Symmetry (mesh properties `use_mirror_x/y/z`, `use_mirror_vertex_groups`, `use_mirror_topology`): **Mirror X/Y/Z** mirror strokes across the local axes; **Mirror Vertex Groups** paints on groups with symmetrical names (a group with no counterpart paints symmetrically on the active group itself); **Radial X/Y/Z** repeats strokes; **Topology Mirror** uses topology-based mirroring. To change the axis directions, rotate the model in Edit Mode, not Object Mode.

## Gotchas
- A mesh that is not symmetric leaves unmatched vertices unchanged.
- With Mirror Weights and one vertex selected the unselected vertex's data overwrites it; check which side you selected.

## Verify
Pose a bone and its mirrored bone with equal and opposite rotations and compare the deformation from the front.

## Checked
Date: 2026-10-27. Documentation: Blender manual, Weight Paint Editing and Symmetry pages, branch blender-v5.2-release. Confirmed: Mirror tool options and semantics, the opposite-bone recipe, symmetry settings, naming conventions. Removed unconfirmed claims: Vertex Groups panel specials menu as a second location, the 0.0001 tolerance, centre-line averaging, local-X rotation advice, Copy Pose and Paste X-Flipped verification, the Symmetrize snap tip, and the property name in the option label (UI label is Mirror Vertex Groups).
Run check, 2026-11-01, Blender 4.5.14 LTS headless on a 5x5 grid with groups Arm.L (left vertices at 0.7) and Arm.R (empty): Mirror Weights with Arm.R active copied nothing from Arm.L (it mirrors within the active group, which is why the opposite-bone recipe duplicates and renames the group first); Flip Group Names with Arm.L active moved the left vertices into Arm.R at weight 0.7 and left Arm.L empty; operator defaults as written above. Unrun: the duplicate-and-rename recipe end to end, All Groups, Topology Mirror results, brush symmetry, the rotate-in-Edit-Mode advice.
Method: documentation checked against the manual and API pages; the code and operators were run headless in Blender 4.5.14.
