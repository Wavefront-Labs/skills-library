---
id: creative-arts.animation.blender.bpy-keyframe-api
name: bpy-keyframe-api
category: creative-arts
field: animation
product: blender
tags: [blender, bpy, python, bpy-keyframe-api, keyframe-insert, animation-data-api, fcurves]
level: practitioner
status: verified
description: "Animate from Python: keyframe_insert with data paths and frames, fast keyframe_points add and foreach_set, interpolation, slotted actions and reading F-curves."
sources:
  - https://docs.blender.org/api/current/bpy.types.bpy_struct.html#bpy.types.bpy_struct.keyframe_insert
  - https://docs.blender.org/api/current/bpy.types.FCurveKeyframePoints.html
  - https://docs.blender.org/api/current/bpy_extras.anim_utils.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# bpy-keyframe-api

Goal: generate or edit animation with code (procedural motion, mocap cleanup, data-driven animation).

## Simple: keyframe_insert

```python
ob.location = (0, 0, 0); ob.keyframe_insert(data_path="location", frame=1)
ob.location.z = 2;       ob.keyframe_insert(data_path="location", index=2, frame=24)
pb = arm.pose.bones["hand.L"]; pb.keyframe_insert("rotation_quaternion", frame=10)
mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].keyframe_insert("default_value", frame=1)
```
`index=-1` (default) keys all components. The call also adds F-curves and animation data when necessary. Prefer the direct route below for thousands of keys.

## Fast: write keyframe points directly

```python
import numpy as np
# fc: the F-curve for location Z, found or created as shown below
frames = np.arange(1, 1001, dtype=np.float32); values = np.sin(frames * 0.1)
fc.keyframe_points.add(len(frames))
fc.keyframe_points.foreach_set("co", np.column_stack([frames, values]).ravel())
for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
fc.update()
```

## Finding F-curves (versions differ)

- Older releases: `ob.animation_data.action.fcurves.find("location", index=2)` or `.new(...)`.
- Blender 5.2 uses **slotted actions** (actions with slots, layers, strips and channelbags); `Action` has no `fcurves` property in the 5.2 API. Use the channelbag helper in `bpy_extras.anim_utils`, `action_get_channelbag_for_slot(action, slot)` (returns the first channelbag for the slot, or None), then `channelbag.fcurves`. Check your version's API docs.
- `ob.animation_data_create()` makes sure animation data exists.
- Blender 4.5.14 still has `Action.fcurves` next to slots and layers, and both routes found the same curves: `action.fcurves.find("location", index=2)` and `anim_utils.action_get_channelbag_for_slot(action, ob.animation_data.action_slot).fcurves`. Keys inserted through `keyframe_insert` default to Bezier interpolation with Auto Clamped handles.

## Interpolation and handles

`kp.interpolation` ('CONSTANT', 'LINEAR', 'BEZIER'), `kp.handle_left_type` / `handle_right_type` ('AUTO_CLAMPED', 'VECTOR', ...), `kp.easing`. Call `fc.update()` after editing so handles recalculate.

## Gotchas

- Rotation mode: key `rotation_euler` or `rotation_quaternion` to match the object's `rotation_mode`.
- After inserting keys by script, `scene.frame_set(scene.frame_current)` re-evaluates the animation at the current frame.

## Verify

Open the Graph Editor: curves have the expected keys and interpolation. Scrub: motion matches the data.

## Checked

2026-10-27 against the Blender 5.2 Python API (bpy_struct.keyframe_insert signature, bpy_extras.anim_utils.action_get_channelbag_for_slot, Action page). Confirmed `Action.fcurves` is absent in 5.2; removed the unconfirmed 4.4 compatibility history and the redraw claim. Run check, 2026-11-01, Blender 4.5.14 LTS headless: `keyframe_insert("location")` created curves for indices 0-2 and index=2 reused curve 2; the numpy `foreach_set("co", ...)` fast path with 1000 points evaluated correctly (value at 1.5 equals the mean of sin(0.1) and sin(0.2)); node-socket `keyframe_insert("default_value")` worked; Keyframe interpolation/easing/handle enums. Unrun: that `Action.fcurves` is absent in 5.2 (4.5.14 still has it), pose-bone keying, the frame_set re-evaluation note.

Method: documentation checked against the 5.2 API pages; the code was run headless in Blender 4.5.14.
