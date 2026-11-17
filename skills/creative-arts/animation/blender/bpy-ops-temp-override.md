---
id: creative-arts.animation.blender.bpy-ops-temp-override
name: bpy-ops-temp-override
category: creative-arts
field: animation
product: blender
tags: [blender, bpy, python, bpy-ops-vs-data, bpy-ops, temp-override, context-override]
level: practitioner
status: verified
description: "Choose between bpy.ops operators and direct data API, and run context-dependent operators with context.temp_override, including finding windows, areas and regions."
sources:
  - https://docs.blender.org/api/current/bpy.ops.html
  - https://docs.blender.org/api/current/bpy.types.Context.html#bpy.types.Context.temp_override
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# bpy-ops-temp-override

Goal: scripts that are fast and do not fail with "context is incorrect".

## Prefer the data API

Operators (`bpy.ops.*`) depend on context and return only a status set. The data API is direct and does not need a UI context:

| Instead of | Use |
|---|---|
| `bpy.ops.object.select_all(action='DESELECT')` | `for o in context.selected_objects: o.select_set(False)` |
| `bpy.ops.mesh.primitive_cube_add()` | `bpy.data.meshes.new()` + `from_pydata` or bmesh |
| `bpy.ops.object.modifier_add(type='SUBSURF')` | `ob.modifiers.new("Subsurf", 'SUBSURF')` |
| `bpy.ops.object.material_slot_add()` | `ob.data.materials.append(mat)` |
| `bpy.ops.anim.keyframe_insert()` | `ob.keyframe_insert("location")` |

## When an operator is needed

Some actions only exist as operators (applying modifiers, many import/export functions, UV unwrap). Call them with the right context:

```python
import bpy
win = bpy.context.window_manager.windows[0]
area = next(a for a in win.screen.areas if a.type == 'VIEW_3D')
region = next(r for r in area.regions if r.type == 'WINDOW')
with bpy.context.temp_override(window=win, area=area, region=region, active_object=ob, selected_objects=[ob]):
    bpy.ops.object.modifier_apply(modifier="Subsurf")
```
`Context.temp_override(window=, screen=, area=, region=, **keywords)` is a context manager that temporarily overrides context members. Only override what the operator reads. The previous context is restored on leaving the block, also when the block raises, and an unknown keyword such as `bogus=1` is accepted without error, so a typo in a member name silently does nothing.

## Diagnosing

- `bpy.ops.x.y.poll()` returns False when context is wrong. Check it before calling.
- A poll failure usually means a missing area, mode or active object in the context.
- Some operators need a specific mode: `bpy.ops.object.mode_set(mode='EDIT')` with an active object.

## Gotchas

- Background mode (4.5.14, factory startup) does have one window whose screen has Properties, Outliner, Dope Sheet and 3D Viewport areas, so the snippet above runs there, but do not assume it: use `next(..., None)` and fall back to the data API or bmesh. Without an override, `bpy.ops.view3d.view_selected.poll()` is False and calling it raises RuntimeError ("expected a view3d region"); `bpy.ops.anim.keyframe_insert.poll()` is also False, so use `ob.keyframe_insert("location")`.
- Prefer the data API inside loops over many objects; operators need a valid context on every call.

## Verify

The script works in `blender -b` and in the UI.

## Checked

2026-10-27 against the Blender 5.2 Python API (Context.temp_override signature, bpy.ops, Object.select_set, keyframe_insert). Removed unconfirmed claims (version gates, undo-step and depsgraph cost, error text, timing). Run check, 2026-11-01, Blender 4.5.14 LTS headless: `modifier_apply` on a Subsurf modifier through `temp_override(active_object=, selected_objects=)` returned FINISHED (cube went to 26 vertices) and the snippet with window, area and region from `windows[0]` also ran; inside that override `context.area.type`, `space_data.type` and `region.type` were VIEW_3D, VIEW_3D and WINDOW, and `view3d.view_selected` finished; `select_all(action='DESELECT')`, `mode_set`, `material_slot_add` and `uv.smart_project` ran in background mode; `modifiers.new`, `data.materials.append`, `keyframe_insert` and the deselect loop over `context.selected_objects` replaced the operators as the table says; `.poll()` exists on operators and returned False for the 3D view operator outside an override; the override restored `active_object` and cleared `selected_objects` after an exception. Unrun: UI sessions with several windows, undo behaviour.
Method: documentation checked against the manual and API pages; the code and operators were run headless in Blender 4.5.14.
