---
id: computing-software.game-programming.godot.pixel-perfect-2d-settings
name: pixel-perfect-2d-settings
category: computing-software
field: game-programming
product: godot
tags: [godot, godot-2d, pixel-perfect, integer-scaling, stretch-mode, game-programming]
level: practitioner
status: docs-checked
description: "Configure Godot 4 stretch mode, stretch aspect and integer scale mode for pixel-art games, with a base size that scales without black bars."
sources: ["https://docs.godotengine.org/en/stable/tutorials/rendering/multiple_resolutions.html", "https://docs.godotengine.org/en/stable/tutorials/2d/2d_transforms.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pixel-perfect 2D settings

**Goal:** sharp, evenly sized pixels at any window size.

## Project settings (Display > Window)
- Set the base window size to the native resolution you design at. The Godot docs note most
  pixel-art games use viewport sizes between 256x224 and 640x480, and that 640x360 scales to
  1280x720, 1920x1080, 2560x1440 and 3840x2160 without black bars under integer scaling.
- **Stretch Mode**:
  - `viewport`: the scene renders to a viewport at the base size, which is then scaled to fit
    the screen (taking Stretch Aspect into account). The Scale setting divides the viewport
    resolution, making pixels look larger.
  - `canvas_items`: 2D elements are scaled relative to the base window size, then multiplied by
    the Scale setting. The docs recommend `canvas_items` plus aspect `expand` for supporting many
    resolutions and aspect ratios in general.
- **Stretch Aspect**: `keep` retains the viewport size and adds black bars (letterboxing);
  `expand` keeps the aspect ratio but keeps neither base width nor height, so more of the
  world shows on other aspect ratios; `keep_width` / `keep_height` and `ignore` also exist.
- **Stretch Scale Mode**: the default is `fractional` (any scale factor, such as 2.133x).
  `integer` rounds the scale factor down, e.g. 2.5 becomes 2.0, and fills the remaining space
  with black bars so each viewport pixel is a whole NxN block of screen pixels. The docs show
  this with the `viewport` stretch mode on pixel art.
- Rendering > 2D has snap options for transforms and vertices (see the 2D transforms page).

## Gotchas
- With integer scale mode, a fullscreen mode that reduces height by one pixel can force a
  smaller scale factor; the multiple-resolutions page covers this.
- Stretch aspect has no effect when Stretch Mode is Disabled.
- Test stretch settings with game embedding set to Stretch to Fit, as the docs advise, so the
  viewport matches the window size.

## Verify
- [ ] Screenshot at a larger window: every art pixel is a uniform NxN block.

## Checked
2026-11-01. Confirmed on Godot docs "Multiple resolutions" (stretch modes, aspect values,
fractional vs integer behaviour and 2.5 to 2.0 example, 640x360 baseline, recommended
canvas_items + expand, embedding note). Removed: texture filter and mipmap settings, camera
smoothing and rounding advice, movement jitter, UI/SubViewport and font advice, "4.2+" version
note, snap-option descriptions.
Method: documentation only; no commands were run.
