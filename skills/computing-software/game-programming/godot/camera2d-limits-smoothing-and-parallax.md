---
id: computing-software.game-programming.godot.camera2d-limits-smoothing-and-parallax
name: camera2d-limits-smoothing-and-parallax
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-2d, camera2d, parallax2d, camera-limits, position-smoothing, drag-margins, screen-shake, game-programming]
level: intro
status: docs-checked
description: "Set up Godot Camera2D for 2D games: following, drag margins, position smoothing, level limits from a TileMap, screen shake via offset, and Parallax2D backgrounds."
sources: ["https://docs.godotengine.org/en/stable/classes/class_camera2d.html", "https://docs.godotengine.org/en/stable/tutorials/2d/2d_parallax.html", "https://docs.godotengine.org/en/stable/classes/class_parallax2d.html", "https://docs.godotengine.org/en/stable/classes/class_tilemaplayer.html", "https://docs.godotengine.org/en/stable/classes/class_tileset.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Camera2D limits, smoothing and parallax

**Goal:** a 2D camera that follows the player smoothly, never shows outside the level, shakes on
impacts, and has layered parallax backgrounds.

## Following
Make `Camera2D` a child of the player (simplest) or a separate node that copies the player's position
(better when the player can be destroyed). Pick the active camera with `make_current()`
or `enabled` (default true).

## Feel settings
- `position_smoothing_enabled` (default false) + `position_smoothing_speed` (default 5.0).
- `drag_horizontal_enabled` and `drag_vertical_enabled` (both default false), with `drag_left_margin`,
  `drag_right_margin`, `drag_top_margin`, `drag_bottom_margin` (default 0.2): the camera moves only
  when the player leaves the drag area.
- `process_callback = Camera2D.CAMERA2D_PROCESS_PHYSICS` (default is `CAMERA2D_PROCESS_IDLE`) when the
  player moves in `_physics_process`, to avoid jitter between physics and render frames.

## Limits from the level
```gdscript
func fit_to_tilemap(cam: Camera2D, layer: TileMapLayer) -> void:
    var r := layer.get_used_rect()
    var cell := layer.tile_set.tile_size
    cam.limit_left = r.position.x * cell.x
    cam.limit_top = r.position.y * cell.y
    cam.limit_right = r.end.x * cell.x
    cam.limit_bottom = r.end.y * cell.y
```
`limit_smoothed = true` eases into limits instead of stopping abruptly. For rooms (Metroidvania), set
limits per room when the player enters its area.

## Screen shake via offset
```gdscript
var trauma := 0.0
func add_trauma(a: float) -> void: trauma = min(trauma + a, 1.0)
func _process(delta: float) -> void:
    trauma = max(trauma - delta * 1.5, 0.0)
    var s := trauma * trauma
    offset = Vector2(randf_range(-1, 1), randf_range(-1, 1)) * 16.0 * s
    rotation = randf_range(-1, 1) * 0.05 * s     # needs ignore_rotation = false
```
Use `offset`, not `position`, so shake does not fight following/limits.
## Parallax2D (Godot 4.3+)
Add `Parallax2D` nodes (one per layer) with child sprites; set `scroll_scale` (0.2 far mountains, 0.5
hills, 1.0 = moves with world) and `repeat_size` (texture width) + `repeat_times` for infinite tiling.
`autoscroll` for clouds. Replaces the older `ParallaxBackground`/`ParallaxLayer` pair (still available).

## Verify
- [ ] Camera never shows beyond the level edges in any room.
- [ ] No jitter on the player sprite while moving and smoothing is on.
- [ ] Parallax layers tile seamlessly at the level's widest point.

## Checked
2026-10-28, Godot docs `stable` (latest release tag 4.7.2-stable). Confirmed from the Camera2D, Parallax2D, TileMapLayer, TileSet class pages and the 2D parallax tutorial: drag_*, position_smoothing_*, limit_* names and defaults, make_current(), enabled, ignore_rotation default true, CAMERA2D_PROCESS_PHYSICS/IDLE, get_used_rect(), tile_size, Parallax2D scroll_scale/repeat_size/repeat_times/autoscroll, Parallax2D since 4.3. Fixed: process_callback enum name (was PHYSICS). Removed: physics interpolation 4.3+ claim, one-current-camera claim, FastNoiseLite tip, 0..1 half-screen margin wording.
Method: documentation only; no commands were run.
