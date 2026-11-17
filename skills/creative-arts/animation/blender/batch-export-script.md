---
id: creative-arts.animation.blender.batch-export-script
name: batch-export-script
category: creative-arts
field: animation
product: blender
tags: [blender, batch-export-script, batch-export, fbx-export, gltf-export, collection-exporters, pipeline]
level: practitioner
status: verified
description: "Export many objects, collections or .blend files to FBX, glTF or USD from a script: per-object loops, collection exporters, per-file subprocesses and naming rules."
sources:
  - https://docs.blender.org/api/current/bpy.ops.export_scene.html
  - https://docs.blender.org/manual/en/latest/scene_layout/collections/collections.html#exporters
  - https://docs.blender.org/api/current/bpy.ops.wm.html
  - https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# batch-export-script

Goal: one command turns a kit file into 200 engine-ready files with consistent names and settings.

## Option A: per object inside one Blender

```python
import bpy, os
out = bpy.path.abspath("//export")
os.makedirs(out, exist_ok=True)
view_layer = bpy.context.view_layer
for ob in [o for o in bpy.data.collections["EXPORT"].all_objects if o.type == 'MESH']:
    for o in view_layer.objects: o.select_set(False)
    ob.select_set(True); view_layer.objects.active = ob
    saved = ob.matrix_world.copy()
    ob.matrix_world.translation = (0, 0, 0)        # export at origin
    bpy.ops.export_scene.fbx(filepath=os.path.join(out, f"SM_{ob.name}.fbx"),
                             use_selection=True, apply_scale_options='FBX_SCALE_ALL',
                             object_types={'MESH'}, use_mesh_modifiers=True, bake_anim=False)
    ob.matrix_world = saved
```
glTF: `bpy.ops.export_scene.gltf(filepath=..., use_selection=True, export_apply=True)` (`export_format='GLB'` writes one binary file; `'GLTF_SEPARATE'` writes a .gltf plus a .bin; both ran in 4.5.14). USD: `bpy.ops.wm.usd_export(filepath=..., selected_objects_only=True)`.

## Option B: Collection Exporters

Collection properties → *Exporters* → add an exporter per collection (the manual lists Alembic, USD, OBJ, PLY, FBX (legacy) and glTF) and set its file path and options. *File → Export All Collections* (`bpy.ops.wm.collection_export_all()`) runs every configured exporter for all collections; the panel's *Export All* button does it for the active collection.

## Option C: many .blend files

One Blender process per file (memory stays clean and one bad file does not stop the batch):

```bash
for f in kits/*.blend; do blender -b "$f" --python-exit-code 1 --python export_one.py -- --out export/ || echo "FAILED $f" >> failures.txt; done
```

## Gotchas

- With `use_selection=True` only selected objects are exported; select them first (as the loop does).
- Engines differ in how they treat unapplied scale (practice); apply transforms in the source or use the exporter's scale options consistently.
- Names: spaces and dots cause trouble in many engines (practice); sanitise (`re.sub(r"[^A-Za-z0-9_]", "_", name)`).
- Restore anything you change (transforms, selection) or the .blend is altered if saved later.

## Verify

Count files written vs objects in the collection; re-import a sample into an empty scene and check scale, origin and materials; the failure log is empty.

## Checked

Blender 5.2 manual (blender-v5.2-release) and Python API 5.2, read 2026-10-27.
- `bpy.ops.export_scene.fbx` arguments use_selection, apply_scale_options='FBX_SCALE_ALL', object_types, use_mesh_modifiers, bake_anim; `bpy.ops.export_scene.gltf` arguments export_format, use_selection, export_apply; `bpy.ops.wm.usd_export(selected_objects_only=)`; `bpy.ops.wm.collection_export_all()`: API 5.2.
- Collection exporters panel, supported formats, File > Export All Collections: manual collections page. `--python-exit-code <code>` (0-255) exists: command-line arguments page.
- Removed as unconfirmed: the GLB enum value (not shown in the operator docs), the 4.2 version tag, background-mode export and where settings are stored.

Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): ran export_scene.fbx with the skill's arguments (use_selection, apply_scale_options='FBX_SCALE_ALL', object_types={'MESH'}, use_mesh_modifiers, bake_anim=False) on a selected mesh and got a file; ran export_scene.gltf with use_selection, export_apply and export_format 'GLB' and 'GLTF_SEPARATE' and read the JSON back; wm.usd_export has selected_objects_only; wm.collection_export_all exists. Not run (confirmed from the manual only): the collection exporter panel, the per-file shell loop and --python-exit-code, engine behaviour with scale and names.

Method: manual text confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.
