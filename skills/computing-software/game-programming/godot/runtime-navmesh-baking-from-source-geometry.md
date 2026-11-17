---
id: computing-software.game-programming.godot.runtime-navmesh-baking-from-source-geometry
name: runtime-navmesh-baking-from-source-geometry
category: computing-software
field: game-programming
product: godot
tags: [godot, godot-navigation, navigation-mesh-source-geometry, runtime-navmesh-bake, navigationserver, game-programming]
level: practitioner
status: docs-checked
description: "Bake Godot navigation meshes at runtime: NavigationRegion bake_navigation_mesh on threads, parsing source geometry, NavigationServer baking APIs and procedural levels."
sources: ["https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationmeshes.html", "https://docs.godotengine.org/en/stable/classes/class_navigationserver3d.html", "https://docs.godotengine.org/en/stable/classes/class_navigationmesh.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Runtime navmesh baking from source geometry

**Goal:** navigation for procedurally generated or player-modified levels, baked without freezing the
game.

## Simple route: NavigationRegion3D
```gdscript
@onready var region: NavigationRegion3D = $NavigationRegion3D
func rebuild():
    region.bake_navigation_mesh(true)        # on_thread = true
    await region.bake_finished
```
The NavigationMesh resource settings decide what's parsed:
- `geometry_parsed_geometry_type`: Mesh Instances, Static Colliders, or Both.
- `geometry_source_geometry_mode`: root node children, groups (with/explicit) — tag procedural pieces
  with a group and bake by group.
- `agent_radius`, `agent_height`, `agent_max_climb`, `agent_max_slope`, `cell_size`/`cell_height`
  (`cell_size` should match the navigation map's cell size, Project Settings > Navigation > 3D).

## Server route (more control)
```gdscript
var nav_mesh := NavigationMesh.new()
var src := NavigationMeshSourceGeometryData3D.new()
NavigationServer3D.parse_source_geometry_data(nav_mesh, src, level_root)   # main thread: reads scene
NavigationServer3D.bake_from_source_geometry_data_async(nav_mesh, src, func():
    region.navigation_mesh = nav_mesh)                                       # bakes on worker thread
```
Parsing must happen on the main thread (reads the scene tree); baking can be async. Add geometry
manually with `src.add_mesh(mesh, xform)` / `add_faces()` for things not in the tree.

## Chunked worlds
Bake per chunk into separate NavigationRegion3D nodes; set `navigation_mesh.filter_baking_aabb` (and
`filter_baking_aabb_offset`) to the chunk bounds, and use `border_size` to bake seamless tiles. Regions
connect when their edges are within the map edge connection margin (project setting
`navigation/3d/default_edge_connection_margin`).

## 2D
NavigationRegion2D with NavigationPolygon: outlines + `NavigationServer2D.bake_from_source_geometry_data`
or the region's `bake_navigation_polygon()`; TileMap navigation polygons per tile can also be used.

## Gotchas
- Check `region.is_baking()` or `NavigationServer3D.is_baking_navigation_mesh(nav_mesh)` before starting another bake of the same mesh.
- Agents query the map one physics frame after changes (map sync); paths requested in the same frame
  may use old data or return an empty path; use a deferred call or wait for `NavigationServer3D.map_changed`.
- A too small `cell_size` or `cell_height` creates so many voxels that it can freeze or crash the game.

## Verify
- [ ] Generate a level, bake on thread: frame time stays stable during bake.
- [ ] Agents path through all procedural connections (debug navigation visible).

## Checked

2026-10-25, against godot-docs master ("latest" docs, last commit 2026-10-24). Confirmed in the using-NavigationMeshes tutorial and the NavigationServer3D, NavigationMesh, NavigationRegion3D and NavigationMeshSourceGeometryData3D class pages: parse_source_geometry_data (main thread only), bake_from_source_geometry_data_async with optional callback, add_mesh and add_faces, filter_baking_aabb, border_size, is_baking and is_baking_navigation_mesh, map_changed, and the voxel-count warning. Removed engine version gates and the claim that a second bake errors.

Method: documentation only; no commands were run.
