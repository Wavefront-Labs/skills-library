---
id: creative-arts.animation.blender.vertex-group-assign
name: vertex-group-assign
category: creative-arts
field: animation
product: blender
tags: [blender, vertex-groups, vertex-group-assign, assign-vertex-group, edit-mode, skinning]
level: practitioner
status: docs-checked
description: "Assign exact vertex group weights in Blender Edit Mode: Assign, Remove, Select, Deselect, Ctrl-G menu, the Vertex Weights panel and group specials."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/properties/vertex_groups/assigning_vertex_group.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/properties/vertex_groups/vertex_groups.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/properties/vertex_groups/vertex_weights.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# vertex-group-assign

Goal: numeric, selection-based weights for rigid parts and masks.

## Vertex Groups panel (Edit Mode, Object Data tab)
- Plus adds a group (named "Group"), minus removes the active group (only the assignments, not the vertices). Click an entry to make it active; the padlock locks it (locked groups can only be renamed or deleted).
- Select vertices, set **Weight**, click **Assign**: selected vertices are added to the active group with that weight. Assign is additive (existing members stay) and sets the weight of all selected vertices to the Weight value.
- **Remove**: removes selected vertices from the active group. **Select** / **Deselect**: select or deselect the vertices in the active group; both are additive to the current selection.
- The same operations are in the 3D Viewport's Vertex > Vertex Groups menu, shortcut Ctrl-G. The panel also has Auto Normalize (keeps bone-deforming groups summing to 1.0 while weight painting or assigning).
- Ungrouped vertices: Select > Select All by Trait > Ungrouped Vertices.

## Vertex Weights panel (Sidebar, Edit Mode, or Weight Paint with vertex selection)
Shows the groups of the **active vertex** (the last selected, highlighted white) with editable weights (type, drag, or arrows for 0.01 steps), filter buttons for deform and other groups, **Delete Weight**, **Normalize** (active vertex sums to 1.0, relative magnitudes kept), **Copy** (copy all weights of the active vertex to other selected vertices) and **Paste Weight to Selected** (copy one weight). These buttons are disabled if a locked group is in the current filter list. Enable *Vertex Group Weights* in the Mesh Edit Mode Overlays popover to see weights in Edit Mode.

## Group specials menu
Sort by Name, Duplicate Vertex Group (adds a "_copy" group with the same weights), Copy Vertex Group to Selected (to other selected objects with matching vertex indices, such as deformed copies), Mirror Vertex Group (and Topology variant), Remove from All Groups, Clear Active Group, Delete All Unlocked Groups, Delete All Groups, Lock All, Unlock All, Lock Invert All.

## Uses
Rigid mechanical parts: assign a whole part to its bone's group at 1.0. Masks: modifiers and other tools take a vertex group, so build them with Assign at chosen weights.

## Gotchas
- Assign does not remove other members; use Remove to drop vertices.
- Deleting a group never deletes vertices.
- A vertex can belong to several groups, each with its own weight.

## Verify
Deselect all, make the group active, click Select: exactly the intended vertices highlight.

## Checked
Date: 2026-10-27. Documentation: Blender manual, Vertex Groups pages (Assigning, Panel, Vertex Weights), branch blender-v5.2-release. Confirmed: panel buttons and semantics, Ctrl-G and the Vertex menu, Vertex Weights panel buttons, specials menu entries, ungrouped-vertex selection path. Removed unconfirmed claims: Sort by bone hierarchy details, an N-panel Item tab name, L to select linked advice, and the split-mesh gotcha.
Method: documentation only; no commands were run.
