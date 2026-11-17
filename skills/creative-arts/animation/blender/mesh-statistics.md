---
id: creative-arts.animation.blender.mesh-statistics
name: mesh-statistics
category: creative-arts
field: animation
product: blender
tags: [blender, mesh-statistics, statistics-overlay, poly-count, triangle-count, optimization, scene-statistics]
level: intro
status: docs-checked
description: "Measure polygon budgets in Blender: Statistics overlay, status bar scene statistics, evaluated versus base counts with modifiers, triangle counts and Python counting for reports."
sources:
  - https://docs.blender.org/manual/en/latest/editors/3dview/display/overlays.html
  - https://docs.blender.org/manual/en/latest/interface/window_system/status_bar.html
  - https://docs.blender.org/api/current/bpy.types.Object.html
  - https://docs.blender.org/api/current/bpy.types.Mesh.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# mesh-statistics

Goal: know the real vertex, face and triangle counts of an asset against its budget.

## Viewport

- Viewport Overlays → **Statistics**: shows the number of objects (selected and total) and the geometry counts (vertices, edges, faces, triangles, or bones depending on mode and object type). The counters depend on the current selection.
- Status bar: right-click the status bar (or use Preferences > Interface > Status Bar) to enable *Scene Statistics*, which shows information about the data in the active scene.
- The viewport counts reflect what is evaluated in the viewport, so Subdivision viewport levels apply, not render levels (practice; confirm on your file).

## Budget checks

- Game engines typically count triangles, and their vertex counts can be higher than Blender's because UV seams and hard edges split vertices (practice).
- Set the Subdivision viewport level equal to the export level when measuring, or check counts after applying.

## Python report

```python
import bpy
dg = bpy.context.evaluated_depsgraph_get()
for ob in bpy.context.selected_objects:
    if ob.type != 'MESH':
        continue
    ev = ob.evaluated_get(dg)
    me = ev.to_mesh()
    me.calc_loop_triangles()
    print(f"{ob.name}: verts {len(me.vertices)}, faces {len(me.polygons)}, tris {len(me.loop_triangles)}")
    ev.to_mesh_clear()
```
`ob.data` gives the base (pre-modifier) mesh; the evaluated object's mesh includes the modifiers. The Python API documents `Object.to_mesh`, `Object.to_mesh_clear` and `Mesh.calc_loop_triangles` used above (the script itself was not run).

## Gotchas

- Instanced geometry shares data; do not confuse instance counts with unique geometry (practice).

## Verify

The Python report should match the Statistics overlay for the same viewport subdivision level.

## Checked

2026-10-27, Blender manual branch blender-v5.2-release; Python API docs.blender.org/api/current. Confirmed against editors/3dview/display/overlays.rst (Statistics wording), interface/window_system/status_bar.rst (Scene Statistics, right-click choice) and the current Python API pages for Object.to_mesh / to_mesh_clear and Mesh.calc_loop_triangles (docs.blender.org/api/current, fetched on this date). Removed unconfirmed claims about hidden objects, instances and engine counts as fact.

Method: documentation only; no commands were run.
