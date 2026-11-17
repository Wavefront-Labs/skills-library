---
id: computing-software.game-programming.godot.astargrid2d-grid-pathfinding
name: astargrid2d-grid-pathfinding
category: computing-software
field: game-programming
product: godot
tags: [godot, godot-navigation, astargrid2d, grid-pathfinding, tactics-movement, game-programming]
level: practitioner
status: verified
description: "Use Godot's AStarGrid2D for tile and tactics games: region and cell size, diagonal modes, heuristics, solid and weighted cells, jumping, and syncing with TileMapLayer."
sources: ["https://docs.godotengine.org/en/stable/classes/class_astargrid2d.html", "https://docs.godotengine.org/en/stable/classes/class_astar2d.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AStarGrid2D for grid games

**Goal:** fast grid pathfinding for roguelikes, tactics and tile-based games without building graphs by
hand.

## Setup
```gdscript
var grid := AStarGrid2D.new()
func build_from(layer: TileMapLayer):
    grid.region = layer.get_used_rect()
    grid.cell_size = Vector2(16, 16)                    # so get_point_path returns world-ish positions
    grid.diagonal_mode = AStarGrid2D.DIAGONAL_MODE_ONLY_IF_NO_OBSTACLES
    grid.default_compute_heuristic = AStarGrid2D.HEURISTIC_OCTILE
    grid.default_estimate_heuristic = AStarGrid2D.HEURISTIC_OCTILE
    grid.update()                                        # must call after changing region, cell size or offset
    for cell in layer.get_used_cells():
        var data := layer.get_cell_tile_data(cell)
        if data and data.get_custom_data("solid"): grid.set_point_solid(cell, true)
        elif data: grid.set_point_weight_scale(cell, data.get_custom_data("cost"))
```
Path:
```gdscript
var cells: Array[Vector2i] = grid.get_id_path(from_cell, to_cell)          # grid coordinates
var pts: PackedVector2Array = grid.get_point_path(from_cell, to_cell)      # positions (cell_size * id + offset)
```
4.3+: `get_id_path(from, to, allow_partial_path=false)`; pass `true` to get a path to the closest reachable cell when the target is unreachable. The default is `false` (4.7.2 class reference), and with a solid target and the default the result was an empty array. The docs warn that `allow_partial_path = true` with a solid target can take unusually long.

## Options
- Diagonal modes: ALWAYS, NEVER, AT_LEAST_ONE_WALKABLE, ONLY_IF_NO_OBSTACLES (no corner cutting). With one blocked neighbour, going (0,0) to (2,2): ONLY_IF_NO_OBSTACLES detoured `[(0,0),(0,1),(1,2),(2,2)]`, AT_LEAST_ONE_WALKABLE and ALWAYS cut the corner `[(0,0),(1,1),(2,2)]`, NEVER stepped orthogonally.
- Heuristics: Euclidean, Manhattan (4-way), Octile (8-way), Chebyshev. Match heuristic to movement or
  paths look odd / searches get slow.
- `jumping_enabled = true` enables jumping (Jump Point Search style) to skip intermediate points and speed up the search; the docs note that weight scaling is not considered while it is on (run: path `[(0,0),(3,3)]` on an open grid).
- `offset` to shift returned positions to cell centers (`cell_size / 2`).
- `cell_shape` (4.3+): `CELL_SHAPE_SQUARE`, `CELL_SHAPE_ISOMETRIC_RIGHT`, `CELL_SHAPE_ISOMETRIC_DOWN` for isometric maps.

## Tactics movement range
AStarGrid2D has no flood fill; compute reachable cells with your own Dijkstra/BFS using
`is_point_solid` and weights, then call `get_id_path` for the chosen destination.

## Dynamic changes
`set_point_solid` at runtime is cheap; no `update()` needed for solids/weights. Occupied cells (units)
can be toggled solid for the mover's query and restored.

## Gotchas
- Points outside `region` error; check `grid.is_in_boundsv(cell)`.
- Forgetting `update()` after setting region leaves an empty grid: `get_id_path` logs `Can't get id path. Point (0, 0) out of bounds`, and after changing `offset` or `cell_size`, `set_point_solid` and `get_point_path` log `Grid is not initialized. Call the update method.`
- AStar2D/3D (graph based) for non-grid waypoint graphs instead.

## Verify
- [ ] Paths avoid corner cutting with ONLY_IF_NO_OBSTACLES.
- [ ] Benchmark 100 paths/frame on the largest map with and without jumping.
## Checked
Ran on Godot 4.7.2 headless: the `build_from` function exactly as written against a `TileMapLayer` with a `TileSet` carrying `solid` and `cost` custom data (region `P: (0, 0), S: (5, 5)`, solid cell detected, weight 3.0, path routed around the solid cell: `[(0,2),(1,1),(2,1),(3,1),(4,2)]`); `get_id_path` and `get_point_path` (`(2,2)` gives `(32, 32)` with 16-pixel cells and `(40, 40)` after `offset = Vector2(8, 8)` plus `update()`); diagonal mode results; partial path default; `is_in_boundsv`; dirty-grid errors; solids set after `update()` leave the grid clean. `allow_partial_path` and `cell_shape` first appear in the 4.3 class reference (absent in 4.2); jumping note and `offset` note from the 4.7.2 `AStarGrid2D` reference.
