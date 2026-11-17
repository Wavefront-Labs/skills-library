---
id: computing-software.computer-graphics-engineering.graphics-math.mesh-cleanup-and-repair
name: mesh-cleanup-and-repair
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, geometry-processing, mesh-repair, non-manifold, watertight-mesh, pymeshlab, trimesh]
level: practitioner
status: draft
description: "Repair broken meshes: merge duplicate vertices, remove degenerate faces, fix non-manifold edges and flipped normals, fill holes, and make watertight for printing or booleans."
sources: ["https://pymeshlab.readthedocs.io/en/latest/", "https://trimesh.org/", "https://www.open3d.org/docs/release/tutorial/geometry/mesh.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mesh cleanup and repair

## Typical defects
Duplicate vertices (split along UV/normal seams on export), zero-area/degenerate triangles,
non-manifold edges (shared by more than 2 faces) and vertices, inconsistent winding, holes,
self-intersections, tiny disconnected components.

## trimesh (quick)
```python
import trimesh
m = trimesh.load("in.obj", force="mesh", process=True)   # process merges duplicate verts
m.update_faces(m.nondegenerate_faces()); m.update_faces(m.unique_faces())
m.remove_unreferenced_vertices()
trimesh.repair.fix_winding(m); trimesh.repair.fix_inversion(m); trimesh.repair.fix_normals(m)
trimesh.repair.fill_holes(m)
print(m.is_watertight, m.is_winding_consistent, m.euler_number)
```

## PyMeshLab (heavier repairs)
```python
import pymeshlab as ml
ms = ml.MeshSet(); ms.load_new_mesh("in.ply")
ms.meshing_remove_duplicate_vertices(); ms.meshing_remove_duplicate_faces()
ms.meshing_remove_null_faces(); ms.meshing_repair_non_manifold_edges(method=0)
ms.meshing_repair_non_manifold_vertices()
ms.meshing_remove_connected_component_by_diameter(mincomponentdiag=ml.PercentageValue(2))
ms.meshing_close_holes(maxholesize=100)
ms.save_current_mesh("out.ply")
```

## Watertight from garbage
When topology is hopeless (scans, game meshes with intersecting parts): voxel remesh / flood fill
(Blender Remesh modifier, ManifoldPlus, `manifold3d`, or TSDF fusion of rendered depth) or Poisson
reconstruction from points+normals. Loses sharp features unless resolution is high.

## Welding seams
Merge by position with a tolerance relative to the bounding box (e.g. 1e-6 x diagonal); welding
across UV seams destroys UVs, so weld for geometry processing on a copy and keep the original for
rendering.

## Verify
Check: watertight, single component (or expected count), consistent winding, positive volume,
Euler characteristic matching expected genus (V - E + F = 2 - 2g for closed surfaces).
