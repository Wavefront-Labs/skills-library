---
id: creative-arts.animation.blender.shape-key-transfer-mirror
name: shape-key-transfer-mirror
category: creative-arts
field: animation
product: blender
tags: [blender, shape-keys, shape-key-mirror, mirror-shape-key, join-as-shapes, transfer-shape-key, blend-from-shape, topology-mirror]
level: practitioner
status: docs-checked
description: "Move shape data around in Blender: Flip (and topology flip), New from Objects, Update from Objects, Transfer Shape Key operator, and Blend From Shape in Edit Mode."
sources:
  - https://docs.blender.org/manual/en/5.2/animation/shape_keys/shape_keys_panel.html
  - https://docs.blender.org/api/current/bpy.ops.object.html
  - https://docs.blender.org/api/current/bpy.ops.mesh.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# shape-key-transfer-mirror

## Flip (Shape Key Specials menu)

- **Flip** mirrors the shape keys on the X axis in Object Mode (`bpy.ops.object.shape_key_mirror`, "mirror the current shape key along the local X axis"). It does not work unless the mesh vertices are perfectly symmetrical; use Mesh > Symmetrize in Edit Mode first.
- **Flip (Topology)** (`use_topology=True`): detects mirrored vertices from topology, so the mesh does not need to be perfectly symmetrical; both sides need matching, unique topology.
- To make `brow_up_R` from `brow_up_L`: Duplicate the key, then Flip, then rename.

## New from Objects (formerly Join as Shapes)

- Select the object(s) to copy from, then the target object (active), then Specials > **New from Objects** (`bpy.ops.object.join_shapes`): adds the vertex positions of selected objects as new shape keys, or updates existing keys with matching names.
- **New from Objects Flipped** does the same while mirroring across local X (for example make a Left Smile from a Right Smile); topology of all meshes must match.
- **Update from Objects** and **Update from Objects Flipped** update existing keys of the active object from selected objects that have matching key names (useful for symmetrical and pose-corrective shapes).
- Use when shapes are sculpted on a duplicate or in another app: the vertex count and order must match.

## Transfer Shape Key (operator)

`bpy.ops.object.shape_key_transfer(mode='OFFSET'|'RELATIVE_FACE'|'RELATIVE_EDGE', use_clamp=False)` copies the active shape key of another selected object to the active one. The 5.2 manual's Specials list has this entry commented out, so confirm it appears in your menu before relying on it.

## Blend From Shape (Edit Mode)

`bpy.ops.mesh.blend_from_shape` and `bpy.ops.mesh.shape_propagate_to_all` are the Edit Mode shape key operators the manual lists; use Blend From Shape to repair a key locally or mix parts of keys. The manual page has no detail on its options, so check the redo panel.

## Gotchas

- Vertex order must match for New from Objects; imports that reorder or merge vertices break it.
- Flip uses local X, so a rotated or off-centre object mirrors wrongly.

## Verify

Toggle the L and R keys: identical magnitude, mirrored; a joined key at 1 matches its source object.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release source) and Python API reference: Specials menu names and behaviour (Flip, Flip (Topology), New from Objects (Flipped), Update from Objects (Flipped)), operator signatures for `shape_key_mirror`, `join_shapes`, `shape_key_transfer`, existence of `mesh.blend_from_shape`. Corrected: menu names (Mirror Shape Key is Flip, Join as Shapes is New from Objects). Removed as unconfirmed: reported-failure-count message, OBJ export advice, Data Transfer modifier tip, Blend From Shape factor/Add option details.
Method: documentation only; no commands were run.
