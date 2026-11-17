---
id: creative-arts.animation.blender.legacy-pose-library
name: legacy-pose-library
category: creative-arts
field: animation
product: blender
tags: [blender, pose-library, legacy-pose-library, convert-pose-library, pose-markers, migration]
level: practitioner
status: docs-checked
description: "Recover poses from old Blender pose libraries (actions with pose markers) as pose assets via a script around poselib.create_pose_asset, then check catalogs and flipping."
sources:
  - https://docs.blender.org/manual/en/5.2/animation/armatures/posing/editing/pose_library.html
  - https://docs.blender.org/api/current/bpy.types.Action.html
  - https://docs.blender.org/api/current/bpy.ops.poselib.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# legacy-pose-library

Goal: recover hand/face poses from an old rig file where the pose library was an action with **pose markers** (the old Pose Library panel) into the asset-based pose library.

## Status in the current manual and API

- The Blender 5.2 manual describes only the asset-based pose library; the old Sidebar Pose Library panel now just has a button to open the asset shelf.
- The 5.2 Python API lists these poselib operators: `apply_pose_asset`, `asset_delete`, `asset_modify`, `blend_pose_asset`, `copy_as_asset`, `create_pose_asset`, `paste_asset`, `pose_asset_select_bones`, `restore_previous_action`. There is no conversion operator.
- `Action.pose_markers` still exists ("markers specific to this Action, for labeling poses").
- Whether a conversion operator existed in older releases is not covered by the current docs: check the manual of the Blender version the file came from.

## Scripted conversion (Pose Mode, relevant bones selected)

```python
import bpy
ob = bpy.context.object
act = bpy.data.actions["PoseLib"]          # the legacy library action
ob.animation_data.action = act
ob.animation_data.action_slot = act.slots[0]
for m in act.pose_markers:
    bpy.context.scene.frame_set(m.frame)
    bpy.ops.poselib.create_pose_asset(pose_name=m.name)
ob.animation_data.action = None
```

- `create_pose_asset(pose_name, asset_library_reference, catalog_path)` stores keys for the selected bones only, so select the bones that belong to each pose type first (loop per bone subset if needed).
- Actions are slotted since 4.4, so assign a slot as shown (see `action-slots`).
- Run it on a copy of the file first; this recipe was written from the API reference and was not executed.

## After conversion

- Assign catalogs (`catalog_path`) and regenerate thumbnails with Generate Preview (see `pose-asset-creation`).
- Pose assets can be modified later with Adjust Pose / Replace / Add / Remove.

## Gotchas

- Legacy libraries often keyed every bone at every pose; assets that hold only the relevant bones are more useful.
- Pose markers belong to the action; they are not scene timeline markers.

## Verify

Each converted asset applies the same pose as its marker frame in the original file.

## Checked

2026-10-27, Blender 5.2 manual and Python API reference: poselib operator list and `create_pose_asset` signature, `Action.pose_markers`, slot assignment properties, asset modify modes. Removed as unconfirmed: the 3.0-3.6 "Convert Legacy Pose Library" operator, 4.4 versioning wording.
Method: documentation only; no commands were run.
