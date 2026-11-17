---
id: creative-arts.animation.blender.stl-3d-print-export
name: stl-3d-print-export
category: creative-arts
field: animation
product: blender
tags: [blender, stl, stl-export, 3mf, 3d-print-export, 3d-printing, manifold, print-toolbox]
level: practitioner
status: verified
description: "Export print-ready meshes from Blender: STL exporter options (scale, units, ASCII/binary, batch), manifold checks, and the 3D Print Toolbox extension."
sources:
  - https://docs.blender.org/manual/en/latest/files/import_export/stl.html
  - https://extensions.blender.org/add-ons/print3d-toolbox/
  - https://docs.blender.org/manual/en/latest/scene_layout/scene/properties.html
  - https://docs.blender.org/api/current/bpy.ops.wm.html#bpy.ops.wm.stl_export
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# stl-3d-print-export

Goal: a file the slicer accepts at the right size first time.

## Scene setup

- Scene Properties > Units: *Unit System* Metric, *Length* Millimeters, *Unit Scale* 0.001 so 1 Blender unit = 1 mm and dimensions read in mm. The manual notes that Unit Scale only changes the values displayed in the interface. (Or keep metres and set the export *Scale* to 1000.)
- Apply scale (`Ctrl A` > Scale) and all modifiers you need, or enable *Apply Modifiers* on export.

## Check printability (3D-Print Toolbox extension, N panel > 3D-Print)

- The extension's listing says it can calculate mesh volume and surface area, check for bad geometry and fix it with *Make Manifold*, hollow a model, rotate it by aligning selected faces to the print bed, scale it to given boundaries or volume, and quick-export the selection to STL, PLY or OBJ. Open its panel after installing it to see the exact tools and settings.
- Core alternative: Edit Mode *Select > Select All by Trait > Non Manifold* (vertex or edge select mode).

## STL export (File > Export > STL)

- *Format: ASCII* (off = binary), *Batch* (each object as a separate file), *Include: Selection Only*, *Scale*, *Scene Unit* (apply the scene's unit scale to the exported data), *Forward / Up* axes (operator defaults Y forward, Z up), *Apply Modifiers* (on by default). The 4.5.14 STL exporter has no Viewport or Render Properties option.
- STL itself has no unit field, so confirm the size in the slicer (practice; most slicers assume mm).

## 3MF

Search the Get Extensions tab for a 3MF add-on if your slicer prefers it; its features and slicer support were not checked here.

## Gotchas

- A size wrong by 1000x points to a unit-scale or export-scale mismatch; check the dimensions in the sidebar before export.
- Flipped normals and internal faces left by booleans are common causes of slicer repair warnings (practice); recalculate normals outside and clean up before export.

## Verify

Open in the slicer: size equals the sidebar dimensions and no repair warnings appear; compare the volume with the 3D Print Toolbox volume readout. Run: a 2-unit cube exports a 684-byte binary file (80-byte header, 4-byte count, 12 triangles of 50 bytes); `ascii_format=True` starts with `solid`; `global_scale=1000` writes vertices at plus or minus 1000.

## Checked

Blender 5.2 manual (files/import_export/stl, scene properties, mesh select-all-by-trait) and Python API 5.2 (`bpy.ops.wm.stl_export` with ascii_format, use_batch, export_selected_objects, global_scale, use_scene_unit, forward_axis='Y', up_axis='Z', apply_modifiers), read 2026-10-27; extensions.blender.org 3D Print Toolbox page (version 1.5.0, GPL-3.0-or-later, Blender 4.2 LTS and newer).
- STL options, Unit System / Unit Scale / Length, Select All by Trait > Non Manifold (vertex/edge modes): manual pages.
- Removed as unconfirmed: the specific toolbox check names and the wall-thickness and overhang thresholds, the Shift Ctrl Alt M shortcut, the 4.1 exporter tag, and the 3MF extension claims (the guessed extension URL did not resolve).

Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): bpy.ops.wm.stl_export options ascii_format, use_batch, export_selected_objects, global_scale, use_scene_unit, forward_axis Y, up_axis Z, apply_modifiers (no Properties option); cube exports in binary, ASCII and scaled forms with the sizes and content quoted. Not run (confirmed from the manual only): the Unit System and Unit Scale advice, the 3D-Print Toolbox extension features and the slicer behaviour.

Method: manual text and shipped UI scripts confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.
