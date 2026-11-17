---
id: creative-arts.animation.blender.usd-export-import
name: usd-export-import
category: creative-arts
field: animation
product: blender
tags: [blender, usd, usd-export, usd-import, usdz, import-export, pipeline, openusd]
level: practitioner
status: verified
description: "Move scenes between Blender and USD pipelines: USD export options (selection, animation, materials, instancing, root prim, USDZ), import options, scale/up-axis and known gaps."
sources:
  - https://docs.blender.org/manual/en/latest/files/import_export/usd.html
  - https://docs.blender.org/api/current/bpy.ops.wm.html#bpy.ops.wm.usd_export
  - https://openusd.org/release/index.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# usd-export-import

Goal: exchange layout, animation and lookdev with Houdini/Omniverse/Maya/Apple tools via `.usd/.usda/.usdc/.usdz`.

## Export (File > Export > Universal Scene Description)

- **Scope** (Blender 4.5.14 also has `visible_objects_only`, on by default, and `use_instancing`, off by default, which the 5.2 manual does not list): all visible, supported objects are exported, optionally limited by *Selection Only*; invisible objects, USD layers and variants are not supported. Supported types: meshes, cameras (perspective only), curves, text (as meshes), lights, hair (as curves, parent strands only), point clouds, metaballs, volumes, armatures.
- **Animation**: when checked the entire scene frame range is exported (otherwise only the current frame); the evaluated mesh is written, so deforming and topology-changing meshes work. *Incremental Save* reduces peak memory.
- **Root Prim** (`root_prim_path`, default `/root`): adds a transform prim with the given path as the parent of all exported data.
- **Blender Data**: *Custom Properties* (with *Namespace*), *Blender Names*, *Allow Unicode* (needs USD 24.03 or newer on the reading side).
- **Geometry**: *UV Maps*, *Rename UV Maps* (`st` instead of `UVMap`), *Normals*, *Triangulate*, *Merge parent Xform*. **Rigging**: *Shape Keys* (absolute shape keys unsupported), *Armatures* as USD skeletons (bendy bones unsupported), *Only Deform Bones*.
- **Materials**: the exporter approximates Principled BSDF as a *USD Preview Surface Network* (a *MaterialX Network* option also exists); one geometry subset per material. *Relative Paths* (File References) use relative paths for textures and volumes.
- **USDZ**: set the output file extension to `.usdz` to write a zip archive containing the USD and its texture dependencies (run: a cube exports a zip holding one `c.usdc`). A `.usdc` extension writes binary (`PXR-USDC` magic) and `.usda` writes ASCII (`#usda 1.0`).
- **Convert Orientation**, **Forward / Up Axis**, **Units** (writes the stage `metersPerUnit`) and **Xform Ops** (Translate/Rotate/Scale, Translate/Orient/Scale, or Matrix).
- **Use Settings for**: Viewport or Render.

## Import

- File > Import > USD can import cameras, curves, lights, materials, meshes, point clouds, primitive shapes and volumes. Options include *Path Mask* (import only the subset rooted at a prim), *Scale*, *Set Frame Range*, *Create Collection*, *Apply Unit Conversion Scale* (scales by the stage `metersPerUnit`, in addition to *Scale*), *Light Intensity Scale*, *Scene Instancing* (USD instances become collection instances), *Import All Materials*, *Import Textures* (for USDZ) and *Material Name Collision*.
- A Y-up stage gets a rotation on root objects to match Blender's Z up.
- *Import USD Preview* converts USD Preview Surface shaders to Principled BSDF nodes; the manual says this can be lossy.
- Animation: time-varying transforms add a Transform Cache constraint and animated geometry a Mesh Sequence Cache modifier; file sequences (one file per frame) are not supported.

## Gotchas

- Neither the exporter nor the importer handles USD layers, variants or references; compose those in another tool (practice: a Python `pxr` script is one option).
- Prim names: *Blender Names* writes the original object and data names as custom attributes, which helps downstream tools that must map back by name.

## Verify

Open the exported file in `usdview` (or save as an ASCII `.usda` from a USD tool) and check the prim hierarchy, `upAxis`, `metersPerUnit` and time samples.

## Checked

Blender 5.2 manual (blender-v5.2-release, files/import_export/usd) read 2026-10-27; `bpy.ops.wm.usd_export(selected_objects_only=, export_materials=)` argument names confirmed in API 5.2.
- Supported object types, animation behaviour, Root Prim, custom properties, geometry/rigging options, material approximation and displacement notes, USDZ via file extension, Units/Xform Ops, import options, animation import (Transform Cache constraint, Mesh Sequence Cache modifier), Y-up conversion: manual USD page.
- Corrected: the 5.2 manual lists no Visible Only or instancing export option, although the 4.5.14 operator has both; removed unconfirmed version tags, `.usdc`/`.usda` extension behaviour, the Export Textures option, MaterialX import claims and the Reality Converter advice.

Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): bpy.ops.wm.usd_export option list (selected_objects_only, visible_objects_only, export_animation, export_uvmaps, rename_uvmaps, export_normals, export_materials, export_armatures, only_deform_bones, export_shapekeys, evaluation_mode RENDER/VIEWPORT, generate_preview_surface, generate_materialx_network, convert_orientation, xform_op_mode TRS/TOS/MAT, root_prim_path, export_custom_properties with userProperties namespace, author_blender_name, allow_unicode, merge_parent_xform, convert_scene_units, meters_per_unit, relative_paths) and usd_import (scale, set_frame_range, create_collection, prim_path_mask, apply_unit_conversion_scale, light_intensity_scale, support_scene_instancing, import_all_materials, import_usd_preview, mtl_name_collision_mode, import_textures_mode); a cube exported to .usdc, .usdz and .usda (metersPerUnit 1, upAxis Z, defaultPrim root) and the .usdc re-imported as one mesh with 8 vertices. Not run (confirmed from the manual only): supported object types, the animation export behaviour, the lossy-material remark, and the layers and variants limits.

Method: manual text and shipped UI scripts confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.
