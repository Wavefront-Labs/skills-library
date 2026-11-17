---
id: creative-arts.animation.blender.rna-paths
name: rna-paths
category: creative-arts
field: animation
product: blender
tags: [blender, rna-paths, data-path, copy-data-path, path-resolve, bpy, drivers]
level: practitioner
status: docs-checked
description: "Work with RNA data paths: copy data path and full path, path_resolve and path_from_id, F-curve data paths and indices, escaping names and debugging broken paths."
sources:
  - https://docs.blender.org/api/current/bpy.types.bpy_struct.html#bpy.types.bpy_struct.path_resolve
  - https://docs.blender.org/api/current/info_quickstart.html
  - https://docs.blender.org/api/current/bpy.utils.html#bpy.utils.escape_identifier
  - https://developer.blender.org/docs/release_notes/4.4/python_api/
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# rna-paths

Goal: address any property as a string for drivers, keyframes, overrides and scripts.

## Copy paths from the UI

- Right-click → *Copy Data Path* (`Shift Ctrl C`): path relative to the ID, e.g. `modifiers["Bevel"].width`.
- *Copy Full Data Path* (`Shift Ctrl Alt C`): `bpy.data.objects["Cube"].modifiers["Bevel"].width`.
- Drivers and F-curves always store the **relative** path plus an *array index* for vectors (`location` index 2 = Z).

## Resolve in Python

```python
ob = bpy.data.objects["Cube"]
ob.path_resolve('modifiers["Bevel"].width')            # value
ob.path_resolve('modifiers["Bevel"].width', False)     # bpy_prop: the property itself
mod = ob.modifiers["Bevel"]
mod.path_from_id("width")                               # 'modifiers["Bevel"].width'
from bpy_extras import anim_utils
ad = ob.animation_data
cb = anim_utils.action_get_channelbag_for_slot(ad.action, ad.action_slot)
for fc in cb.fcurves:                                   # F-curves live in channelbags (slotted actions)
    print(fc.data_path, fc.array_index)
```

## Building paths safely

Names with quotes or backslashes must be escaped:

```python
from bpy.utils import escape_identifier
name = 'Bone "A"'
path = f'pose.bones["{escape_identifier(name)}"].location'
```

## Common paths

| What | Path (relative to ID) |
|---|---|
| Pose bone rotation | `pose.bones["hand.L"].rotation_quaternion` |
| Pose bone custom prop | `pose.bones["CTRL"]["ik_fk"]` |
| Shape key value | on the Key ID: `key_blocks["smile"].value` |
| Material node input | on the material: `node_tree.nodes["Principled BSDF"].inputs[2].default_value` |
| Geometry nodes modifier input | `modifiers["GeometryNodes"]["Socket_2"]` (use Copy Data Path to get the real identifier) |

## Gotchas

- Shape key and material paths live on their own IDs (Key, Material), not the object; keyframes go into those IDs' animation data.
- Prefer node input names (`inputs["Roughness"]`) over indices (practice).
- After renaming a bone or modifier, check that drivers on other objects and your scripts still use the new name (practice).

## Verify

`ob.path_resolve(path)` returns the expected value for every path you store; the Drivers editor shows no invalid paths.

## Checked

Blender Python API 5.2 and developer-docs release notes 4.4, read 2026-10-27.
- `bpy_struct.path_resolve(path, coerce=True)`, `path_from_id(property='')`, `bpy.utils.escape_identifier(string)`: API 5.2. Copy Data Path shortcuts: manual interface menus page.
- Corrected a stale snippet: `Action.fcurves` no longer exists in the 5.2 API; F-curves are reached through `bpy_extras.anim_utils.action_get_channelbag_for_slot(action, slot).fcurves` (introduced with slotted actions in 4.4), and `AnimData.action_slot` selects the slot.
- Removed as unconfirmed: the claim that renames update F-curves automatically and the note on node input index changes (kept as practice advice).

Method: documentation only; no commands were run.
