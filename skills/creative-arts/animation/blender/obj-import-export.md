---
id: creative-arts.animation.blender.obj-import-export
name: obj-import-export
category: creative-arts
field: animation
product: blender
tags: [blender, obj-export, obj-import, wavefront-obj, mtl, import-export, interchange]
level: practitioner
status: verified
description: "Exchange meshes as Wavefront OBJ from Blender: importer/exporter options (axes, scale, groups, MTL path modes, triangulate, modifiers) and OBJ's limits."
sources:
  - https://docs.blender.org/manual/en/latest/files/import_export/obj.html
  - https://docs.blender.org/api/current/bpy.ops.wm.html#bpy.ops.wm.obj_export
  - https://paulbourke.net/dataformats/obj/
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# obj-import-export

Goal: reliable static mesh exchange (sculpt apps, CAD viewers, 3D printing services, photogrammetry) with OBJ + MTL.

## Export (File > Export > Wavefront (.obj))

- **Include**: Selected Only (otherwise all objects in the scene). **Apply Modifiers** (`apply_modifiers`, on by default), **Properties** (`export_eval_mode`: Viewport by default, or Render). The 5.2 manual's Apply Transform option does not exist on the 4.5.14 operator; check the export panel in your version.
- **Forward / Up axis** and **Scale**. The operator defaults are -Z Forward, Y Up (the manual notes Blender itself uses Y Forward, Z Up, and that apps with Y up need -Z Forward, Y Up).
- **Geometry**: UV Coordinates, Normals, Colors (written in the "xyzrgb" extension), Curves as NURBS, *Triangulated Mesh*.
- **Grouping**: Object Groups, Material Groups, Vertex Groups, Smooth Groups, Smooth Group Bitflags.
- **Materials**: writes the `.mtl` file; *PBR Extensions* adds roughness, metallic, sheen, clearcoat, anisotropy and transmission. **Path Mode**: *Auto* (relative inside the export folder, absolute outside), *Absolute*, *Relative*, *Match*, *Strip Path* (filename only), *Copy* (copies textures and references them with a relative path; use for handing off).
- **Animation**: exports a numbered OBJ for each frame from Frame Start to End, which can take a long time; for animation prefer a format that carries it (practice).

## Import (File > Import > Wavefront (.obj))

- *Scale*, *Clamp Bounding Box* (clamps files of widely varying scale to a fixed size), forward/up axes, *Split By Object* / *Split By Group*, *Vertex Groups*, *Detect Cyclic Curves*, *Path Separator* (builds a collection hierarchy from object names), *Validate Meshes* (`validate_meshes`, on by default in 4.5.14; checks for corrupt data and fixes it; recommended, since errors can crash display or editing). The 5.2 manual also lists Material Name Collision; the 4.5.14 importer has no such option. Detect Cyclic Curves is `close_spline_loops` (default on) and Path Separator is `collection_separator`.
- A matching `.MTL` file's materials are imported too.

## OBJ limits

- No armatures, lights, cameras, empties, parenting or transformations (per the manual). NURBS surfaces, text and metaballs are converted to meshes at export. OBJ carries no units, so agree a scale with the receiving app (practice).
- Normals are written only with *Normals* enabled; many apps recalculate their own.

## Gotchas

- Absolute paths in MTL break on handoff — use *Copy* or *Relative*.
- Validation makes import slower, but the manual recommends keeping *Validate Meshes* on because data errors are not always obvious.

## Verify

Re-import the exported OBJ into a fresh scene; vertex/face counts and UVs match (Statistics overlay). Run: a default cube exports a `.obj` with 8 `v` lines, `vn` normals and an `mtllib` reference plus a `.mtl`, and re-imports as 8 vertices, 6 faces and one UV map.

## Checked

Blender 5.2 manual (files/import_export/obj) and Python API 5.2 (`bpy.ops.wm.obj_export`, `obj_import`), read 2026-10-27.
- Export and import option lists, Path Mode values, PBR Extensions, Animation (numbered OBJ per frame), compatibility note and supported-content note: manual OBJ page. Operator defaults forward_axis='NEGATIVE_Z', up_axis='Y', export_colors False, clamp_size, validate_meshes, use_split_objects/groups, import_vertex_groups: API 5.2.
- Removed as unconfirmed: a Visible Only limit, `o`/`g` statement mapping, the vn/hard-edge claim and the C++ speed remark. Corrected the Validate advice (the manual recommends keeping it on).

Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): bpy.ops.wm.obj_export option list (export_animation, forward_axis NEGATIVE_Z, up_axis Y, global_scale, apply_modifiers, export_eval_mode, export_selected_objects, export_uv, export_normals, export_colors off, export_materials, export_pbr_extensions, path_mode AUTO/ABSOLUTE/RELATIVE/MATCH/STRIP/COPY, export_triangulated_mesh, export_curves_as_nurbs, group options, smooth_group_bitflags) and obj_import (global_scale, clamp_size, axes, use_split_objects on, use_split_groups off, import_vertex_groups off, validate_meshes on, close_spline_loops, collection_separator); cube export and re-import. Not run (confirmed from the manual only): the numbered-file behaviour of Animation export, the Path Mode semantics, and the OBJ content limits.

Method: manual text and shipped UI scripts confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.
