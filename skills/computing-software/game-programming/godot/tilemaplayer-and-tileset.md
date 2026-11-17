---
id: computing-software.game-programming.godot.tilemaplayer-and-tileset
name: tilemaplayer-and-tileset
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-2d, tilemaplayer, tileset, terrains, autotile, custom-data-layers, tile-physics, set-cell, game-programming]
level: practitioner
status: docs-checked
description: "Build 2D levels with Godot 4 TileMapLayer and TileSet: atlas setup, physics/navigation layers, terrains for autotiling, custom data, and editing cells from code."
sources: ["https://docs.godotengine.org/en/stable/tutorials/2d/using_tilesets.html", "https://docs.godotengine.org/en/stable/tutorials/2d/using_tilemaps.html", "https://docs.godotengine.org/en/stable/classes/class_tilemaplayer.html", "https://docs.godotengine.org/en/stable/classes/class_tileset.html", "https://docs.godotengine.org/en/stable/classes/class_tiledata.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TileMapLayer and TileSet

**Goal:** tile-based 2D levels with collision, navigation, autotiling and gameplay data per tile.
A `TileMapLayer` node holds one layer of tiles; the older multi-layer `TileMap` node is deprecated (use several
TileMapLayer nodes instead).

## TileSet setup
1. Add a `TileMapLayer` and give it a `TileSet` resource (`tile_size` defaults to 16x16).
2. Add an atlas source from a sprite sheet in the TileSet editor.
3. **Physics Layers**: select the TileMapLayer, click the TileSet value in the inspector, unfold
   Physics Layers and Add Element; the same applies to navigation and occlusion layers. Then draw the
   shapes per tile in the TileSet editor.
4. **Custom Data Layers**: name + type (e.g. `damage: int`, `surface: String`), then set values per tile.

## Terrains (autotiling)
Terrains are grouped into terrain sets; each set has a mode: Match Corners and Sides, Match Corners, or
Match Sides. Create the set and its terrains in the TileSet, assign each tile's peering bits, then paint
with terrains in the tile map editor.

## Code access
```gdscript
@onready var ground: TileMapLayer = $Ground

func tile_under(world_pos: Vector2) -> Vector2i:
    return ground.local_to_map(ground.to_local(world_pos))

func damage_at(world_pos: Vector2) -> int:
    var data := ground.get_cell_tile_data(tile_under(world_pos))
    return data.get_custom_data("damage") if data else 0

func break_block(cell: Vector2i) -> void:
    ground.erase_cell(cell)

func place_wall(cell: Vector2i) -> void:
    ground.set_cell(cell, 0, Vector2i(3, 1))                    # source_id, atlas_coords, alternative
    # autotile neighbours with terrains:
    ground.set_cells_terrain_connect([cell], 0, 0)              # terrain_set, terrain
```
`map_to_local(cell)` gives the centre of a cell. `get_used_cells()`, `get_used_rect()` for level bounds.

## Performance and structure
- Use several `TileMapLayer` nodes (background, ground with collision, decoration), each with its TileSet.
- `physics_quadrant_size` (default 16): within a quadrant, cells with similar physics properties are
  grouped and their collision shapes merged. `rendering_quadrant_size` (default 16) groups tiles into one
  canvas item; it does not apply to a Y-sorted layer. Setting `physics_quadrant_size` to 1 disables physics chunking.
- A Scenes Collection in the TileSet editor places whole scenes as tiles.

## Verify
- [ ] Player collides with all solid tiles; no seams catching the player at tile edges.
- [ ] Terrain painting produces correct borders for every used combination.
- [ ] Custom data queries return expected values in a test scene.

## Checked
2026-10-28, Godot docs `stable` (latest release tag 4.7.2-stable). Confirmed from the Using TileSets and Using TileMaps tutorials and the TileMapLayer, TileSet and TileData class pages: TileMap deprecated in favour of TileMapLayer, tile_size default 16x16, physics layer setup, terrain set modes, local_to_map, map_to_local, get_cell_tile_data, get_custom_data, erase_cell, set_cell and set_cells_terrain_connect signatures, get_used_cells/get_used_rect, quadrant sizes (default 16), Scenes Collection. Removed (not confirmed): the 4.3+ gate, 47-tile wording, set_cell(cell, -1) erase, navigation-from-collision tip, peering-bit gotcha, batching advice, z_index per layer.
Method: documentation only; no commands were run.
