---
id: creative-arts.animation.blender.bmesh-mathutils
name: bmesh-mathutils
category: creative-arts
field: animation
product: blender
tags: [blender, bmesh, mathutils, geometry-scripting, python, bpy, vector, matrix, quaternion, kdtree, bvhtree, procedural-mesh, mesh-api, foreach-get, numpy, bmesh-edit-mesh, bmesh-ops, bmesh-layers]
level: advanced
status: verified
description: "Script geometry in Blender: bmesh editing, from_pydata, foreach_get/set with NumPy, mathutils Vector/Matrix/Quaternion/Euler, KDTree and BVHTree queries, and pitfalls."
sources:
  - https://docs.blender.org/api/current/bmesh.html
  - https://docs.blender.org/api/current/bmesh.ops.html
  - https://docs.blender.org/api/current/mathutils.html
  - https://docs.blender.org/api/current/mathutils.bvhtree.html
  - https://docs.blender.org/api/current/bpy.types.Mesh.html
  - https://docs.blender.org/api/current/bmesh.types.html
  - https://docs.blender.org/api/current/bmesh.utils.html
  - https://docs.blender.org/api/current/mathutils.geometry.html
  - https://docs.blender.org/api/current/mathutils.kdtree.html
  - https://docs.blender.org/api/current/mathutils.noise.html
  - https://docs.blender.org/api/current/bpy.types.Object.html
  - https://docs.blender.org/api/current/bpy.types.bpy_prop_collection.html
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# bmesh-mathutils

Goal: generate and modify geometry from Python at speed, without `bpy.ops` and without fighting coordinate spaces.

## Three ways to touch a mesh

| API | Use when |
|---|---|
| `bmesh` | topology edits (extrude, bevel, dissolve, boolean), per-element loops, edit-mode scripts |
| `Mesh.from_pydata(verts, edges, faces)` | building a mesh from lists once (fast, simple) |
| `foreach_get/foreach_set` + NumPy | bulk read/write of positions/attributes on big meshes |
Prefer these APIs over `bpy.ops.mesh.*` in tools.

## bmesh basics

```python
import bmesh, bpy
from mathutils import Vector

me = bpy.data.meshes.new("Gen")
bm = bmesh.new()
v = [bm.verts.new((x, y, 0)) for x, y in [(0,0),(1,0),(1,1),(0,1)]]
f = bm.faces.new(v)                       # verts in winding order
bm.faces.ensure_lookup_table()            # needed before bm.faces[i] after creation/removal
bmesh.ops.extrude_face_region(bm, geom=[f])
bm.to_mesh(me); bm.free()
ob = bpy.data.objects.new("Gen", me); bpy.context.collection.objects.link(ob)
me.update()
```
- **Edit mode round trip**: `bm = bmesh.from_edit_mesh(ob.data)` … edit … `bmesh.update_edit_mesh(ob.data)` (no `to_mesh`, no `free`). Object mode: `bm.from_mesh(me)` → `bm.to_mesh(me)` → `bm.free()`.
- Elements: `bm.verts/edges/faces` (sequences; `.ensure_lookup_table()` before indexing; `.index_update()` to refresh `.index`), `v.co`, `v.normal`, `v.link_edges`, `v.link_faces`, `e.verts`, `e.link_faces`, `e.is_boundary`, `e.is_manifold`, `e.calc_length()`, `f.verts`, `f.edges`, `f.loops`, `f.normal`, `f.calc_area()`, `f.calc_center_median()`, `f.material_index`, `f.smooth`; `l.vert`, `l.edge`, `l.link_loop_next/prev`, `l[uv_layer].uv`. `.select`, `.hide`, `.tag` (scratch flag), `.select_set(True)` + `bm.select_flush(True)` to propagate.
- Creating/deleting: `bm.verts.new`, `bm.edges.new((a,b))`, `bm.faces.new(seq)` (check first with `bm.faces.get(seq)`, which returns the face using those verts or None), `bm.verts.remove(v)`, `bmesh.ops.delete(bm, geom=..., context='VERTS'|'EDGES'|'FACES'|'FACES_ONLY'...)`.
- **Layers** (custom data): `uv = bm.loops.layers.uv.verify()` / `.get("UVMap")`; `dl = bm.verts.layers.deform.verify()` then `v[dl][group_index] = 0.5` (vertex groups); colour attributes: `bm.loops.layers.color` / `bm.verts.layers.color` (Byte) and `.float_color` (Float) — `.new("Col")` or `.get("Col")`; custom attributes `bm.verts.layers.float.new("mask")`, `.int`, `.string`, `.float_vector`; edge flags `e.smooth` and `e.seam`.
- **Ops** (`bmesh.ops`, return dicts of new geometry): `extrude_face_region`, `extrude_edge_only`, `translate(bm, verts=, vec=)`, `scale`, `rotate(cent=, matrix=)`, `transform(matrix=)`, `inset_individual/region`, `bevel(geom=, offset=, segments=, affect='EDGES'|'VERTICES')`, `subdivide_edges(cuts=, use_grid_fill=True)`, `bisect_plane(plane_co=, plane_no=, clear_outer=)`, `remove_doubles(dist=)` (there is no bmesh boolean op — use the Boolean modifier), `dissolve_limit`, `dissolve_verts/edges/faces`, `triangulate`, `join_triangles`, `recalc_face_normals(faces=)`, `reverse_faces`, `holes_fill`, `contextual_create` (the `F` key), `bridge_loops`, `smooth_vert`, `spin`, `mirror`, `symmetrize`, `convex_hull`, `create_cube/uvsphere/icosphere/cone/circle/grid/monkey`, `split_edges`, `duplicate`, `unsubdivide`, `wireframe`, `solidify`, `poke`, `connect_verts`, `weld_verts`, `pointmerge`, `edgenet_fill`, `region_extend`, `find_doubles`.
  Pattern: `ret = bmesh.ops.extrude_face_region(bm, geom=faces); new = [e for e in ret['geom'] if isinstance(e, bmesh.types.BMVert)]; bmesh.ops.translate(bm, verts=new, vec=(0,0,1))`.
- `bm.normal_update()` after moving verts; `bm.calc_volume()`, `bm.calc_loop_triangles()`; `bmesh.utils.face_split`, `edge_split`, `vert_separate`, `loop_separate`.
- Object transforms: bmesh coordinates are **local**. World: `ob.matrix_world @ v.co`; to bake transforms `bmesh.ops.transform(bm, matrix=ob.matrix_world, verts=bm.verts)` then reset `ob.matrix_world.identity()`.

## Bulk data with foreach and NumPy

```python
import numpy as np
me = ob.data; n = len(me.vertices)
co = np.empty(n*3, dtype=np.float32); me.vertices.foreach_get("co", co); co = co.reshape(n, 3)
co[:, 2] += np.sin(co[:, 0]*3) * 0.1
me.vertices.foreach_set("co", co.ravel()); me.update()
# attributes (4.x): a = me.attributes.new("mask", 'FLOAT', 'POINT'); a.data.foreach_set("value", arr)
# normals: me.vertex_normals / me.polygon_normals (read-only), custom normals via me.normals_split_custom_set()
# loops / uv: uv = me.uv_layers.active; uv.uv.foreach_get("vector", buf)   (uv.data is deprecated)
```
`foreach_get` copies a whole property into a buffer in one call, replacing a Python loop. Build meshes: `me.from_pydata(verts, edges, faces)` (lists of tuples; faces as vertex index tuples, any n-gon) → `me.validate(verbose=True)`, `me.update()`. For evaluated (modifier-applied) data: `dg = bpy.context.evaluated_depsgraph_get(); ob_eval = ob.evaluated_get(dg); me_eval = ob_eval.to_mesh()` … `ob_eval.to_mesh_clear()`, or `bpy.data.meshes.new_from_object(ob_eval)` to keep a copy.

## mathutils

- `Vector((x,y,z))`: `.length`, `.normalized()`, `.dot(v)`, `.cross(v)`, `.angle(v)`, `.lerp(v, t)`, `.project(v)`, `.rotate(q)`, `.to_track_quat('Z','Y')` (aim), `.xy/.xz` swizzles, `v.copy()`; `Vector.Fill`; `@` for matrix·vector.
- `Matrix`: `Matrix.Identity(4)`, `Matrix.Translation(v)`, `Matrix.Rotation(angle, 4, 'Z' or axis_vec)`, `Matrix.Scale(f, 4, axis)`, `Matrix.LocRotScale(loc, rot, scale)` (rot must be a Matrix, Quaternion, Euler or None; a plain tuple raises ValueError), `.inverted()`, `.transposed()`, `.decompose()` → (loc, quat, scale), `.to_3x3()`, `.to_euler()`, `.to_quaternion()`, `.normalized()`, `@` composition (right-to-left: `parent @ local`). `ob.matrix_world`, `matrix_local`, `matrix_basis`, `matrix_parent_inverse`; bones: `pose_bone.matrix` (armature space), `.matrix_basis` (local pose), `bone.matrix_local` (rest, armature space); world of a bone = `arm.matrix_world @ pbone.matrix`.
- `Quaternion((w,x,y,z))` or `Quaternion(axis, angle)`: `.slerp`, `.rotation_difference(q)`, `.to_euler('XYZ')`, `.to_axis_angle()`, `.conjugated()`; multiply `q1 @ q2`. Set rotations by mode: `ob.rotation_mode = 'QUATERNION'; ob.rotation_quaternion = q`.
- `Euler((x,y,z), 'XYZ')`: `.to_quaternion()`, `.rotate_axis('Z', a)`, `.make_compatible(other)` (avoid flips when keying).
- `Color`, `geometry` module: `intersect_line_plane`, `intersect_point_line`, `intersect_ray_tri`, `distance_point_to_plane`, `area_tri`, `normal(verts)`, `barycentric_transform`, `tessellate_polygon`, `delaunay_2d_cdt`, `box_fit_2d`, `convex_hull_2d`; `noise` module (`noise.noise(v)`, `fractal`, `turbulence`, `random_unit_vector`).
- `mathutils.kdtree.KDTree(n)`: `insert(co, i)`, `balance()`, `find(co)`, `find_n`, `find_range` — nearest-point searches.
- `mathutils.bvhtree.BVHTree.FromBMesh(bm)` / `FromObject(ob, dg)` / `FromPolygons(verts, polys)`: `ray_cast(origin, direction, dist)` → (loc, normal, index, dist), `find_nearest(co)`, `overlap(other_tree)` — snapping, projection, collision checks; `scene.ray_cast(dg, origin, dir)` and `ob.ray_cast(origin, dir)` (object-local coordinates!) are the object-level equivalents; `ob.closest_point_on_mesh(co)`.

## Recipes

- **Spiral staircase**: loop `Matrix.Rotation(i*step, 4, 'Z') @ Matrix.Translation((r,0,i*h))` applied to a cube bmesh via `bmesh.ops.create_cube` + `transform`; `bm.to_mesh`.
- **Snap selected verts to another mesh**: `bvh = BVHTree.FromObject(target, dg)`; for each v: `loc,_,_,_ = bvh.find_nearest(target.matrix_world.inverted() @ (ob.matrix_world @ v.co))`; `v.co = ob.matrix_world.inverted() @ (target.matrix_world @ loc)`.
- **Select non-quads**: `for f in bm.faces: f.select = len(f.verts) != 4; bm.select_flush_mode(); bmesh.update_edit_mesh(me)`.
- **Aim an object at a target**: `q = (target.location - ob.location).to_track_quat('-Z','Y'); ob.rotation_euler = q.to_euler()`.

## Gotchas

- Call `ensure_lookup_table()` on `bm.verts/edges/faces` before indexing, and again after adding or removing elements.
- Check for an existing face with `bm.faces.get()` before `bm.faces.new`.
- Prefer `foreach_get/foreach_set` to editing `me.vertices[i].co` in a loop; call `me.update()` afterwards.
- `from_edit_mesh` data is invalid after leaving edit mode or after `bpy.ops` calls — re-fetch.
- Matrix multiplication is `@` (see the `mathutils` page examples).
- `v.co.copy()` returns an independent vector; editing `v.co` directly changes the vertex.
- `ob.ray_cast` takes **local** coordinates; `scene.ray_cast` world.
- Euler → key flips: `make_compatible` with the previous frame's Euler before `keyframe_insert`.
- Big meshes: use NumPy `foreach_get/foreach_set` for coordinate-only changes instead of converting to bmesh.

## Verify

- Generated mesh: `me.validate(verbose=True)` reports no fixes (after `recalc_face_normals`).
- foreach round trip: `foreach_get` → `foreach_set` without changes leaves the mesh identical (`np.allclose`).
- BVH snap: snapped verts lie on the target surface (`find_nearest` distance ≈ 0 after snapping) in world space, not offset by object transforms.
- Rotation maths: `Matrix.LocRotScale(l,q,s).decompose()` returns the inputs (within float tolerance).

## Checked

2026-10-28. Confirmed against the Blender Python API docs (bmesh, bmesh.types, bmesh.ops, bmesh.utils, mathutils, mathutils.geometry/kdtree/noise/bvhtree, bpy.types Mesh/Object/Scene/Bone/PoseBone/bpy_prop_collection/Attribute): bmesh element, sequence and layer members, every listed `bmesh.ops` name and the parameters shown (translate, rotate, transform, bevel, subdivide_edges, bisect_plane, remove_doubles, delete contexts), `BVHTree` constructors and return tuples, `KDTree` methods, `Object.ray_cast` (object space) versus `Scene.ray_cast` (world space), `from_pydata`, `validate`, `normals_split_custom_set`, `attributes.new`, `foreach_get/foreach_set`. Fixed: `uv.data` is deprecated, use `uv.uv` with `vector`. Removed: speed and memory figures, exact exception strings, crease and bevel-weight layer names, `interpolate.poly_3d_calc`, the per-face colour recipe, the Face Orientation overlay colour claim.
Run check, 2026-11-01, Blender 4.5.14 LTS headless: every `bmesh.ops` name in the list exists except `boolean` (which does not, as the skill says); extrude_face_region/translate pattern (8 verts, 6 faces, volume 1.0); `bm.faces.get(verts)` returns the face and `faces.new` on an existing face raises ValueError; delete contexts VERTS, EDGES, FACES, FACES_ONLY ran (also EDGES_FACES, FACES_KEEP_BOUNDARY, TAGGED_ONLY exist); bevel (EDGES and VERTICES), subdivide_edges, bisect_plane, triangulate, remove_doubles, inset_region, duplicate, transform, translate, rotate ran; uv, deform (`v[dl][group] = 0.5`), color, float_color, float, int, string, float_vector layers; baking `matrix_world` with `bmesh.ops.transform` then `matrix_world.identity()`; Vector, Matrix, Quaternion, Euler, geometry, KDTree and BVHTree members listed exist; BVHTree ray_cast/find_nearest/KDTree results; `ob.ray_cast` takes object-local coordinates and `scene.ray_cast` world; the snap-to-target recipe put the plane on the cube surface; the non-quad selection recipe selected 8 triangles and 1 ngon; the aim recipe pointed -Z at the target; `make_compatible`; foreach_get/foreach_set round trip, `uv.uv.foreach_get("vector")`, `attributes.new` + `foreach_set`, `vertex_normals`/`polygon_normals`, `evaluated_get` + `to_mesh`/`to_mesh_clear`, `meshes.new_from_object`. Fixed: LocRotScale does not accept a 4-tuple. Unrun: edit-mode round trip, the spiral staircase beyond building 40 vertices, Face Orientation overlay, `bmesh.utils` functions beyond existence.

Method: documentation checked against the manual and API pages; the code was run headless in Blender 4.5.14.
