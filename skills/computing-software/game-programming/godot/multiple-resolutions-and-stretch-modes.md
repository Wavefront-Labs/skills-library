---
id: computing-software.game-programming.godot.multiple-resolutions-and-stretch-modes
name: multiple-resolutions-and-stretch-modes
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-ui, stretch-mode, multiple-resolutions, aspect-ratio, pixel-art, content-scale, game-programming]
level: practitioner
status: docs-checked
description: "Configure Godot for any screen: base resolution, stretch mode (disabled/canvas_items/viewport), aspect handling, integer scaling for pixel art, anchors and safe areas."
sources: ["https://docs.godotengine.org/en/stable/tutorials/rendering/multiple_resolutions.html", "https://docs.godotengine.org/en/stable/tutorials/ui/size_and_anchors.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiple resolutions and stretch modes

**Goal:** the game looks right on 720p to 4K, ultrawide, phones and Steam Deck.

## Settings (Project Settings > Display > Window)
- **Viewport Width/Height**: the base (design) resolution, e.g. 1920x1080 for HD art; 640x360 is a good
  pixel-art baseline (it scales to 720p, 1080p, 1440p and 4K without bars with integer scaling).
- **Stretch Mode**:
  - `disabled` (default): no stretching, one unit is one pixel, and Stretch Aspect has no effect.
  - `canvas_items`: the base size is stretched to cover the window and everything renders at the target
    resolution; 3D is unaffected and 2D sprite pixels no longer map 1:1 to screen pixels (possible scaling
    artifacts). Recommended for most games.
  - `viewport`: render at base resolution and upscale the image: true pixel-art look, everything chunky.
- **Stretch Aspect**:
  - `keep`: fixed aspect, black bars.
  - `expand`: shows more area on wider/taller screens: **most flexible**; design UI with anchors.
  - `keep_width` / `keep_height`: expand in one axis only (e.g. keep_height for side-scrollers: wider screens see more horizontally).
  - `ignore`: stretches (distorts).
- **Stretch Scale Mode** (since 4.2): `fractional` (default, any scale such as 2.5) or `integer` (rounds the
  scale down; use for pixel art). With `disabled` stretch mode it only rounds the Stretch Scale down.
- `Scale` factor for UI size accessibility options at runtime: `get_window().content_scale_factor = 1.25`.

## Pixel art recipe
Base 640x360, Stretch Mode `viewport`, Aspect `keep` or `expand`, Scale Mode `integer`, textures with
Filter = Nearest (Project Settings > Rendering > Textures > Canvas Textures > Default Texture Filter = Nearest),
and position snapping (`Rendering > 2D > Snap > Snap 2D Transforms to Pixel`).

## UI that adapts
- Anchor presets (Full Rect, Top Right...) and Containers; avoid absolute positions.
- Test with Window size override (`window/size/window_width_override`) or resize the running window.
- Mobile notches: `DisplayServer.get_display_safe_area()` and pad the HUD root.
- 3D: render resolution scale (`Rendering > Scaling 3D > Scale`, FSR) is separate from UI stretch.

## Gotchas
- `viewport` mode renders at the base size and stretches the result: sprites cannot sit at sub-pixel
  positions and 3D is low resolution. If you want those, use `canvas_items` instead.

## Verify
- [ ] Test at 1280x720, 1920x1080, 2560x1080 (21:9), 1280x800 (Deck), 2400x1080 (phone): no clipped UI.
- [ ] Pixel art has uniform pixel sizes (integer scaling) at every tested resolution.

## Checked

Checked 2026-10-25 against the Godot 4.7 documentation (godot-docs stable branch, last commit 2026-10-24; latest engine release 4.7.2). Confirmed: Stretch Mode `disabled` is the default and makes Stretch Aspect ineffective, `canvas_items` leaves 3D unaffected, `viewport` renders at the base size; Stretch Aspect `keep`, `keep_width` (expands vertically), `keep_height` (expands horizontally, best for horizontal scrollers), `expand`, `ignore`; Stretch Scale Mode `fractional` (default) and `integer` since 4.2; the pixel-art recommendations (640x360 base, `viewport`, `keep` or `expand`, `integer`); `Window.content_scale_factor`; the project settings `rendering/2d/snap/snap_2d_transforms_to_pixel`, `rendering/textures/canvas_textures/default_texture_filter`, `display/window/size/window_width_override`, `rendering/scaling_3d/scale`; `DisplayServer.get_display_safe_area()`. Removed the unconfirmed 320x180 baseline, integer-plus-expand border, UI blur and MSDF claims.

Method: documentation only; no commands were run.
