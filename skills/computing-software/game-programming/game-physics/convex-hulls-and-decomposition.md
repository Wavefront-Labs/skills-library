---
id: computing-software.game-programming.game-physics.convex-hulls-and-decomposition
name: convex-hulls-and-decomposition
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, convex-decomposition, convex-hull, collision-shapes, game-programming]
level: practitioner
status: verified
description: "Build physics shapes from art: convex hull generation, approximate convex decomposition with V-HACD or CoACD, hull limits and collision cost."
sources: ["https://github.com/SarahWeiii/CoACD", "https://github.com/kmammou/v-hacd", "https://github.com/NVIDIA-Omniverse/PhysX"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Convex hulls and convex decomposition

**Goal:** turn arbitrary concave render meshes into a few convex pieces dynamic bodies can collide with.

## Why convex
GJK/EPA (Jolt's narrow phase queries are all handled by them) and SAT require convex shapes; concave triangle meshes are normally static or kinematic.
Jolt does allow dynamic mesh bodies if you supply mass and inertia and they never collide with other meshes or heightfields, but its docs advise avoiding them
(expensive, and objects can get stuck inside a mesh). Dynamic concave objects normally need a compound of convex hulls.

## Single hull
Quickhull (Barber et al.; implemented by Qhull, which scipy's `ConvexHull` wraps) is fast in practice: 1,000,000 random 3D points took about 0.1 s and gave an 84-vertex hull. Then simplify: engines cap hull size
(PhysX cooking: vertex limit and polygon limit each default 255, range 4-255; Unity convex MeshCollider: 255 triangles). Fewer vertices =
faster support functions, so keep gameplay hulls small.

## Decomposition
- **V-HACD** (Khaled Mammou): voxelises the mesh and recursively splits by planes. Key parameters:
  max hulls, voxel resolution (default 100,000; the README suggests 10,000,000 for best accuracy), max vertices per hull,
  minimum volume error percent. V-HACD 4 does not look for the minimum hull count: you say how many hulls you want, and it
  returns many even for a simple shape. Godot ships it in `thirdparty/vhacd` and Unity's manual points to it.
- **CoACD** (Wei, Liu, Ling and Su, ACM Transactions on Graphics 2022, SIGGRAPH): collision-aware concavity with tree search;
  parameter `threshold` trades hull count for accuracy (Python `coacd.run_coacd(mesh, threshold=..., max_convex_hull=..., max_ch_vertex=...)`;
  on a U-shaped test mesh thresholds 0.02 / 0.05 / 0.2 / 0.5 gave 9 / 3 / 3 / 1 hulls).
- Run offline in the asset pipeline, cache results keyed by mesh hash.

## Practical guidance
- Start with primitives (boxes, capsules, spheres) authored by hand; use decomposition only when
  the shape matters for gameplay (things you can climb into, stack on).
- Keep the hull count per prop small (a handful); hundreds of hulls multiply broad- and narrow-phase cost.
- Thin parts (blades, sheets) need thickness; a flat point set makes Qhull fail (`QhullError: Initial simplex is flat`).
- Check mass properties: compute inertia from the compound, not the render mesh.

## Verify
- Overlay hull wireframes on the mesh in the editor.
- Drop the prop on a table 100 times: no snagging, settles quickly.

## Checked (2026-10-22)
- Ran scipy `ConvexHull` (Qhull): 1e3 / 1e4 / 1e5 / 1e6 random points in 0.001 / 0.002 / 0.011 / 0.105 s; coplanar points raise `QhullError` (flat initial simplex). Removed the unproven O(n log n) statement.
- Ran `coacd` (pip, with trimesh) on a U-shaped mesh: threshold 0.02/0.05/0.2/0.5 gives 9/3/3/1 hulls, summed hull volume 5.36 to 6.36 against mesh volume 5.0 and single-hull volume 6.0; `run_coacd` parameter names read with `inspect.signature`. Ran `vhacdx.compute_vhacd(..., maxConvexHulls=8, resolution=100000)` giving 8 hulls.
- CoACD README citation (authors, TOG) and V-HACD README (version 4, hull count semantics, resolution 10,000,000 suggestion); Godot `thirdparty/README.md` lists vhacd; PhysX `PxConvexMeshDesc.h` (limit 256 note, vertex/polygon limits default 255, range 4-255); Unity manual Mesh Collider page via search (255 triangles).
- Jolt `Docs/Architecture.md` (GJK/EPA narrow phase; 'Dynamic Mesh Shapes' section).
- Removed the unverified '16-32 typical' and '4-16 hulls' budgets and the Blender add-on claim.
