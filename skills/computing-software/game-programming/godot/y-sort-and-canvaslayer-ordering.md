---
id: computing-software.game-programming.godot.y-sort-and-canvaslayer-ordering
name: y-sort-and-canvaslayer-ordering
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, y-sort, canvaslayer, z-index, tilemaplayer, draw-order, game-programming]
level: practitioner
status: docs-checked
description: "Control 2D draw order in Godot 4: y_sort_enabled for top-down depth, z_index and z_as_relative, TileMapLayer y-sort origin, and CanvasLayer for HUD and parallax layers."
sources: ["https://docs.godotengine.org/en/stable/classes/class_canvasitem.html#class-canvasitem-property-y-sort-enabled", "https://docs.godotengine.org/en/stable/tutorials/2d/canvas_layers.html", "https://docs.godotengine.org/en/stable/tutorials/2d/2d_parallax.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Y-sort and CanvasLayer draw ordering

**Goal:** characters walk behind and in front of trees correctly in top-down/isometric 2D, and UI
always draws on top.

## Default order
CanvasItems draw in tree order on their canvas layer; by default children draw on top of their parents,
so a root CanvasItem is behind everything. `z_index` changes this per item; `z_as_relative` (default
true) makes it relative to the parent's z.

## Y-sort
- Set `y_sort_enabled = true` (default false) on the **parent** node (e.g. a "World" Node2D). That node
  and its child CanvasItems with a higher Y position render in front of those with a lower Y. When
  false, they render in scene tree order.
- Sorting uses each node's position, so place a sprite's origin at its **feet** (offset the Sprite2D),
  otherwise tall sprites sort wrong.
- Nodes sort relative to each other only if they have the same `z_index`; use z for categories
  (ground decals z=-1, flying units z=1).
- Camera2D and Light2D enable y-sort automatically where they need it (class page note).
- TileMapLayer: see the TileMapLayer and TileSet class pages for per-layer y-sort settings and the
  tile's Y Sort Origin; keep characters under the same y-sorted parent as the layer.

## CanvasLayer
Separate drawing layers independent of tree order; they depend only on their `layer` number
(see the Canvas layers tutorial):
- HUD: put it in a `CanvasLayer` with a higher `layer` than the world.
- Background parallax: `Parallax2D` (the 2D parallax tutorial recommends it over ParallaxBackground and
  ParallaxLayer; "prior to 4.3" a CanvasLayer with `follow_viewport_enabled` was the approach).

## Gotchas
- `get_global_mouse_position()` returns the position relative to the CanvasLayer that contains the node,
  so it follows that layer's transform.

## Verify
- [ ] Walk around a tree: player occluded only when above its trunk base.
- [ ] HUD unaffected by camera zoom/shake.

## Checked
2026-10-28, Godot docs `stable` (latest release tag 4.7.2-stable). Confirmed from the CanvasItem class page (y_sort_enabled, z_as_relative, same-z rule, tree order, mouse position), the Canvas layers tutorial and the 2D parallax tutorial. Removed (not confirmed in the pages read): z_index range of -4096..4096, nested y-sort rule, Light2D/CanvasModulate-per-layer note, y-sort CPU cost, HUD layer=10 value, per-tile Y Sort Origin wording and the "children of the layer" advice (now points to the class pages).
Method: documentation only; no commands were run.
