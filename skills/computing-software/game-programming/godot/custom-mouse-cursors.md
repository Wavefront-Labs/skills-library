---
id: computing-software.game-programming.godot.custom-mouse-cursors
name: custom-mouse-cursors
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, custom-cursor, mouse, input, ui, game-programming]
level: practitioner
status: docs-checked
description: "Set custom mouse cursors in Godot: project setting, Input.set_custom_mouse_cursor per shape with hotspots, per-Control cursor shapes, and software cursors for size and animation."
sources: ["https://docs.godotengine.org/en/stable/tutorials/inputs/custom_mouse_cursor.html", "https://docs.godotengine.org/en/stable/classes/class_input.html#class-input-method-set-custom-mouse-cursor", "https://docs.godotengine.org/en/stable/classes/class_control.html#class-control-property-mouse-default-cursor-shape"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom mouse cursors

**Goal:** themed cursors that change by context, crisp at any size.

## Global default
Project Settings > Display > Mouse Cursor > **Custom Image** and **Custom Image Hotspot** (pixel of
the click point, e.g. arrow tip at (0,0), crosshair centre at (16,16)).

## From code, per shape
```gdscript
const ARROW := preload("res://ui/cursors/arrow.png")
const HAND  := preload("res://ui/cursors/hand.png")
const CROSS := preload("res://ui/cursors/cross.png")
func _ready() -> void:
    Input.set_custom_mouse_cursor(ARROW, Input.CURSOR_ARROW, Vector2(0, 0))
    Input.set_custom_mouse_cursor(HAND, Input.CURSOR_POINTING_HAND, Vector2(6, 0))
    Input.set_custom_mouse_cursor(CROSS, Input.CURSOR_CROSS, Vector2(16, 16))
```
Controls choose a shape through `mouse_default_cursor_shape`; the custom image for that shape is then used
automatically. Override `_get_cursor_shape()` for region-based
shapes. For world context (hovering an enemy), call `Input.set_default_cursor_shape(Input.CURSOR_CROSS)`.

## Hardware vs software cursors
These are **hardware** cursors: the image must be at most 256x256 (128x128 or smaller is recommended;
128x128 is the maximum on Web) and `hotspot` must lie inside the image. An AnimatedTexture is not
supported (only its first frame shows), so animation means swapping images. For big, animated or shader
cursors: hide the OS cursor (`Input.mouse_mode = Input.MOUSE_MODE_HIDDEN`) and move a
Sprite2D/TextureRect on a top CanvasLayer to `get_viewport().get_mouse_position()` in `_process`. A software
cursor adds at least one frame of latency compared with a hardware cursor; the docs suggest an
extrapolation step to better show the real mouse position.

## Gotchas
- The image can be a Texture2D or Image; Lossless, Lossy or Uncompressed import modes are recommended
  (Video RAM works but is decompressed on the CPU, slowing loading).
- Pass `null` to reset a shape to the system cursor.
- Web: maximum 128x128, and images larger than 32x32 only display while the whole cursor is inside the page.

## Verify
- [ ] Cursor hotspot clicks the exact intended pixel.

## Checked

Checked 2026-10-25 against the Godot 4.7 documentation (godot-docs stable branch, last commit 2026-10-24; latest engine release 4.7.2). Confirmed: Project Settings > Display > Mouse Cursor has Custom Image, Custom Image Hotspot and Tooltip Position Offset; `Input.set_custom_mouse_cursor(image, shape, hotspot)` with a 256x256 limit (128x128 recommended, 128x128 on Web, over 32x32 only when inside the page), `null` resets to the system cursor, AnimatedTexture shows only its first frame, recommended import modes; `Input.set_default_cursor_shape`, `Control.mouse_default_cursor_shape` and `Control._get_cursor_shape`; the `Input.CURSOR_*` constants used; the software cursor note (at least one frame of latency, suggest extrapolation). Removed the unconfirmed HiDPI scaling, button default shape and "no lag" claims.

Method: documentation only; no commands were run.
