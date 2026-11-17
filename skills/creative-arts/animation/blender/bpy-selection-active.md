---
id: creative-arts.animation.blender.bpy-selection-active
name: bpy-selection-active
category: creative-arts
field: animation
product: blender
tags: [blender, bpy-selection-active, select-set, view-layer-active, selection, active-object, bpy]
level: practitioner
status: verified
description: "Select and make objects active from Python correctly: select_set, view_layer.objects.active, deselect all, hidden and excluded objects, and edit-mode element selection."
sources:
  - https://docs.blender.org/api/current/bpy.types.Object.html#bpy.types.Object.select_set
  - https://docs.blender.org/api/current/bpy.types.LayerObjects.html
  - https://docs.blender.org/api/current/info_gotcha.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# bpy-selection-active

Goal: set up selection state so operators act on the right objects, without the 2.7x API that no longer exists.

## Objects

```python
import bpy
vl = bpy.context.view_layer
for ob in vl.objects:              # deselect all without an operator
    ob.select_set(False)
target = bpy.data.objects["Crate"]
target.select_set(True)
vl.objects.active = target          # active object (also what context.object returns)
print(target.select_get(), vl.objects.active.name)
print([o.name for o in bpy.context.selected_objects])
```

- Selection is **per view layer**: `select_set` takes an optional `view_layer=`. `ob.select = True` (2.7x) is gone.
- `bpy.ops.object.select_all(action='DESELECT')` works too but needs a valid context.
- Change selection and the active object via the calls above, not by assigning to `context.selected_objects` or `context.active_object`.

## Objects that refuse

- An object that is not in the view layer (excluded collection, or not linked to the scene) cannot be selected there. Check `ob.name in vl.objects` before `select_set` (call `vl.update()` first if you just toggled `exclude`, because the list is stale until then); `select_set` raises RuntimeError for an object that is not in the view layer, and `select_get` returns False.
- `ob.hide_get()` tests the per-view-layer viewport hiding (the eye icon); change it with `ob.hide_set(False)`. Hidden objects are skipped by most operators, so unhide before running one.

## Edit-mode elements (meshes)

Use bmesh in Edit mode: `bm = bmesh.from_edit_mesh(me)`, then `bm.verts[i].select_set(True)` (selects the associated geometry down: a face also selects its edges and vertices, but de-selecting a vertex does not de-select faces), then `bm.select_flush_mode()` and `bmesh.update_edit_mesh(me)`.

## Bones

Bone selection properties differ between releases: in the 5.2 API the `Bone` page lists `hide_select` (whether the bone can be selected) but no `select` flag, so look up the selection API for your version on the `Bone`, `EditBone` and `PoseBone` pages before scripting it. In Blender 4.5.14 `Bone` and `EditBone` have `select`, `select_head`, `select_tail`, `hide` and `hide_select`, and `PoseBone` has no `select`.

## Gotchas

- Operators read `context`; for background/headless runs pass `selected_objects`/`active_object` through `context.temp_override` instead of relying on selection.
- Setting active does not select; set both when an operator needs "selected and active".

## Verify

`[o.name for o in bpy.context.selected_objects]` lists exactly what you selected and `bpy.context.object` is the intended active object.

## Checked

2026-10-27 against the Blender 5.2 Python API (Object.select_set/select_get/hide_get/hide_set with view_layer argument, LayerObjects.active example, BMVert.select_set, BMesh.select_flush_mode, bmesh.update_edit_mesh, Bone page). Removed unconfirmed claims (RuntimeError text, Mesh element `.select` flags, the 4.x `Bone.select` property which is absent from the 5.2 page, performance remarks). Run check, 2026-11-01, Blender 4.5.14 LTS headless: `select_set`/`select_get`/`vl.objects.active`, `context.selected_objects` and `context.object`; a selected object is not automatically active and an active one is not automatically selected; `select_set(True, view_layer=vl)`; assigning `context.selected_objects` or `context.active_object` raises AttributeError (read-only); `ob.select` does not exist; `hide_set`/`hide_get`; `select_all(action='DESELECT')` ran in background mode; BMFace `select_set(True)` selected 4 verts and 4 edges, and deselecting one vertex left the face selected until `select_flush_mode()` cleared it. Unrun: `temp_override` use with operators, bone selection behaviour.

Method: documentation checked against the manual and API pages; the code was run headless in Blender 4.5.14.
