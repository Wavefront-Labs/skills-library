---
id: creative-arts.animation.blender.bpy-mesh-from-pydata
name: bpy-mesh-from-pydata
category: creative-arts
field: animation
product: blender
tags: [blender, bpy, python, bpy-mesh-from-pydata, from-pydata, mesh-api, procedural-mesh]
level: practitioner
status: verified
description: "Build meshes in Python with Mesh.from_pydata: vertex, edge and face lists, update and validate, UVs, attributes, smooth shading and fast foreach_set alternatives."
sources:
  - https://docs.blender.org/api/current/bpy.types.Mesh.html#bpy.types.Mesh.from_pydata
  - https://docs.blender.org/api/current/bpy.types.AttributeGroupMesh.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# bpy-mesh-from-pydata

Goal: generate meshes from data (terrain from a heightmap, scans, procedural props, imported formats).

## Basic

```python
import bpy
verts = [(0,0,0), (1,0,0), (1,1,0), (0,1,0)]
faces = [(0,1,2,3)]
me = bpy.data.meshes.new("quad")
me.from_pydata(verts, [], faces)      # from_pydata(vertices, edges, faces, shade_flat=True)
me.update()
me.validate(verbose=True)             # True if invalid geometry was corrected or removed
ob = bpy.data.objects.new("quad", me); bpy.context.collection.objects.link(ob)
```

## UVs and attributes

```python
uv = me.uv_layers.new(name="UVMap")
for loop in me.loops:                           # one UV per face corner (loop)
    co = me.vertices[loop.vertex_index].co
    uv.data[loop.index].uv = (co.x, co.y)
h = me.attributes.new("height", 'FLOAT', 'POINT')
h.data.foreach_set("value", [v[2] for v in verts])
```
Shading: `from_pydata` has a `shade_flat=True` argument (faces start flat, the `sharp_face` attribute is set); `me.shade_smooth()` makes every face smooth and `me.shade_flat()` flat.

## Large meshes

`from_pydata` is the simple route. For very large meshes, preallocate and use `foreach_set`:
```python
me.vertices.add(n); me.vertices.foreach_set("co", flat_coords)
me.loops.add(nl);   me.loops.foreach_set("vertex_index", loop_verts)
me.polygons.add(nf); me.polygons.foreach_set("loop_start", starts)
me.update()
```

## Gotchas

- Face winding sets the normal direction (counter-clockwise seen from outside is the usual outward convention). Fix inconsistent winding with bmesh `recalc_face_normals`.
- Duplicate vertices are not merged automatically. Merge by distance with bmesh `remove_doubles`.

## Verify

Enter Edit Mode: face count and vertex count match the input, normals (overlay Face Orientation) point outward.

## Checked

2026-10-27 against the Blender 5.2 Python API (Mesh.from_pydata signature with shade_flat, Mesh.shade_smooth/shade_flat, Mesh.validate signature and return value, Polygon loop_start/loop_total). Removed unconfirmed claims (size thresholds, validate removing duplicate edges, version gates for shade_smooth and auto smooth, loop_total derivation). Run check, 2026-11-01, Blender 4.5.14 LTS headless: `from_pydata` created a `sharp_face` attribute (all True), `shade_flat=False` did not, `shade_smooth()` removed it and `shade_flat()` restored it; `validate()` returned False for a valid quad; the UV loop and the `attributes.new("height", 'FLOAT', 'POINT')` + `foreach_set` code ran; the preallocate route (`vertices.add`, `loops.add`, `polygons.add`, `foreach_set`, `update(calc_edges=True)`) gave 4 edges, 1 polygon and a valid mesh without setting `loop_total`; a counter-clockwise quad has normal +Z; duplicate vertices were kept (3 in, 3 out). Unrun: Edit Mode Face Orientation overlay.

Method: documentation checked against the manual and API pages; the code was run headless in Blender 4.5.14.
