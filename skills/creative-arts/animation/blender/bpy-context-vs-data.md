---
id: creative-arts.animation.blender.bpy-context-vs-data
name: bpy-context-vs-data
category: creative-arts
field: animation
product: blender
tags: [blender, bpy, python, scripting, bpy-context-data, bpy-context, bpy-data]
level: practitioner
status: verified
description: "Know when to use bpy.context vs bpy.data in Blender scripts: active and selected objects, view layer state, background mode with no window, and writing context-free code."
sources:
  - https://docs.blender.org/api/current/bpy.context.html
  - https://docs.blender.org/api/current/bpy.data.html
  - https://docs.blender.org/api/current/info_best_practice.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# bpy-context-vs-data

Goal: scripts that work in the UI, in background mode and from other scripts.

## The difference

- **`bpy.data`**: every datablock in the file (objects, meshes, materials, scenes, collections, images, actions). Independent of what the user is looking at. `bpy.data.objects["Cube"]`, `bpy.data.materials.get("Skin")`.
- **`bpy.context`**: the current state: `context.scene`, `context.view_layer`, `context.object` / `context.active_object`, `context.selected_objects`, `context.mode`, `context.area`, `context.window`. It depends on where the script runs.

## Rules

- Find data by name or by walking collections through `bpy.data`, not through selection, in pipeline scripts. Selection is user state and can be anything.
- Use `context` for tools that act on what the user selected (operators, panels).
- Active object: `context.view_layer.objects.active = ob` (set), `context.active_object` (read).
- Selected: `ob.select_get()` / `ob.select_set(True)` (per view layer).
- Scene in background mode: `bpy.context.scene` is the file's active scene. For multi-scene files, use `bpy.data.scenes["Shot"]` explicitly.

## Background mode

`bpy.app.background` is True when Blender runs without a user interface (`-b`). In Blender 4.5.14 (`-b --factory-startup`) there is still one window (`context.window`, with `context.screen` named Layout), but `context.area`, `context.region` and `context.space_data` are None, so code that reads `context.area.type` or `context.space_data.type` fails with AttributeError ("'NoneType' object has no attribute 'type'"). `context.object` and `context.active_object` are None until you set an active object. Write data-based code (guard UI code with `bpy.app.background`), or create a context override where an operator really needs it (see bpy-ops-temp-override).

## Gotchas

- `bpy.data.objects["Cube"]` raises KeyError if missing (`bpy_prop_collection[key]: key "Cube" not found`). Use `.get()` and handle `None`.
- Datablock names are unique (`ID.name`), so a clashing name is changed (a second object named Cube became Cube.001). Store references to objects in variables, not names, within a script.
- Do not keep Python references to datablocks across removal, undo or file loads: the underlying data can be freed or replaced; using the stale reference raises `ReferenceError: StructRNA of type Object has been removed`. Look the datablock up again by name.

## Verify

Run the script both from the Text Editor and with `blender -b file.blend -P script.py`. Both should give the same result.

## Checked

2026-10-27 against the Blender 5.2 Python API (bpy.app.background, Object.select_set/select_get with per-view-layer argument, Gotchas page on unique names, bpy.context/bpy.data pages). Removed unconfirmed claims (that window/area/region are None, exact error text for removed data, `.001` suffix). Run check, 2026-11-01, Blender 4.5.14 LTS headless: `bpy.app.background` True; `context.window` and `context.screen` exist, `context.area`, `context.region`, `context.space_data` are None; `context.object` is None in an empty scene; `bpy.data.objects["Nope"]` raises KeyError and `.get` returns None; duplicate names became Cube and Cube.001; setting `view_layer.objects.active` made both `context.active_object` and `context.object` return it; `select_set(True)` and `select_get()` worked and `selected_objects` listed it; a removed object raised ReferenceError; a second scene `bpy.data.scenes.new("Shot")` left `context.scene` unchanged. Unrun: running the same script from the Text Editor, which needs a UI session.
Method: documentation checked against the manual and API pages; the code and operators were run headless in Blender 4.5.14.
