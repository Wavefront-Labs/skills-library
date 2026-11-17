---
id: computing-software.game-programming.godot.navigationregion-baking
name: navigationregion-baking
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-navigation, navigationregion, navigationregion3d, navigationmesh, navmesh-baking, agent-radius, source-geometry, runtime-baking, game-programming]
level: practitioner
status: docs-checked
description: "Bake Godot navigation meshes: NavigationRegion3D/2D setup, NavigationMesh agent and cell parameters, source geometry modes, runtime/async rebaking and multiple regions."
sources: ["https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationmeshes.html", "https://docs.godotengine.org/en/stable/classes/class_navigationmesh.html", "https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationregions.html", "https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_different_actor_types.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NavigationRegion baking

**Goal:** a navmesh that matches the level's walkable space for your agent size, rebuilt when the
level changes.

## Setup (3D)
1. Add `NavigationRegion3D` as a parent of (or sibling referencing) the level geometry.
2. Create a `NavigationMesh` resource on it; click **Bake NavigationMesh**.
3. Debug > Visible Navigation to see it in the running game.

## Key NavigationMesh parameters
| Parameter | Guidance |
|---|---|
| `agent_radius` | Agent capsule radius; navmesh is shrunk away from walls by this. |
| `agent_height` | Minimum ceiling clearance. |
| `agent_max_climb` | Step height the agent can walk up. |
| `agent_max_slope` | Max walkable slope in degrees. |
| `cell_size` / `cell_height` | Voxel resolution; must match the navigation map's cell size (Project Settings > Navigation > 3D > Default Cell Size) or you get warnings (`navigation/3d/warnings/navmesh_cell_size_mismatch`). A too small `cell_size` or `cell_height` can create so many voxels that the game freezes or crashes. |
| `geometry_parsed_geometry_type` | Mesh instances, static colliders, or both. Static colliders are usually cleaner than render meshes. |
| `geometry_source_geometry_mode` | Root node children, group (with explicit group name), or group + children. |
| `geometry_collision_mask` | Which physics layers count as walkable/obstacle geometry. |
| `region_min_size` | Removes tiny islands (e.g. tops of crates). |

## 2D
`NavigationRegion2D` + `NavigationPolygon`: draw outlines manually, or bake from source geometry
(`NavigationServer2D.bake_from_source_geometry_data`); static colliders and TileMap colliders can be
parsed as source geometry. TileMaps hold polygons per used cell, so parsing them at runtime is slow.

## Runtime and async baking
```gdscript
@onready var region: NavigationRegion3D = $NavigationRegion3D
func on_door_destroyed() -> void:
    region.bake_navigation_mesh(true)        # on_thread = true (the default): bake in a background thread
    await region.bake_finished
```
For procedural levels: build source geometry via `NavigationServer3D.parse_source_geometry_data` and
`bake_from_source_geometry_data_async`, then assign to the region. Rebaking large areas is costly:
split big worlds into several regions (the NavigationServer connects navmeshes of regions that are
close enough) and rebake only the affected region. Parsing always happens on the main thread because
the SceneTree is not thread-safe.

## Agents of different sizes
Each agent size needs its own navigation mesh baked with an appropriate radius and height, on its own
navigation map; navigation layers distinguish movement types on one map, not sizes.

## Verify
- [ ] Navmesh debug view shows no walkable areas inside walls and no gaps in doorways for the agent radius.
- [ ] Runtime rebake after a change completes without frame hitches (threaded).
- [ ] No cell size mismatch warnings in the output.

## Checked

2026-10-25, against godot-docs master ("latest" docs, last commit 2026-10-24). Confirmed in the using-NavigationMeshes and using-NavigationRegions tutorials and the NavigationMesh, NavigationRegion3D and NavigationServer3D class pages: agent_radius/agent_height/agent_max_climb/agent_max_slope, cell_size and cell_height matching the map, geometry_parsed_geometry_type, geometry_source_geometry_mode, geometry_collision_mask, region_min_size, bake_navigation_mesh(on_thread = true) and bake_finished, bake_from_source_geometry_data_async, main-thread parsing, and the cell size mismatch warning setting. The 2D version gates and the claim that layers separate agent sizes were removed or corrected.

Method: documentation only; no commands were run.
